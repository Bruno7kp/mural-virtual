# coding: utf-8
import datetime
import time

from flask import Blueprint, render_template, request, session, redirect, url_for

from mural.mod_base.auth import logado, Roles, Auth
from mural.mod_base.base_model import json_response, admin_403_response, admin_404_response, data_tables_response
from mural.mod_usuarios import Usuario

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_usuarios.route('/entrar', methods=['GET'])
def entrar():
    erro = request.args.get('erro')
    mensagem = None
    if erro == '1':
        mensagem = 'Credenciais inválidas, tente novamente!'
    elif erro == '2':
        mensagem = 'Sua sessão expirou, faça login novamente!'
    return render_template('login.html', mensagem=mensagem)


@bp_usuarios.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@bp_usuarios.route('/entrar', methods=['POST'])
def login():
    cpf = request.form.get('login')
    senha = request.form.get('senha')
    usuario = Usuario()
    usuario.select_by_login(cpf)
    if usuario.identifier > 0 and Usuario.check_hash(senha, usuario.senha):
        usuario.permanent = True
        session['user'] = usuario.serialize()
        session['time'] = time.time()
        return redirect(url_for('home.admin_home'))
    return redirect(url_for('usuarios.entrar', erro=1))


@bp_usuarios.route('/cadastro', methods=['POST'])
def cadastrar():
    # Cadastro via ajax
    usuario = Usuario()
    usuario.nivel = Roles.usuario.value
    populate_from_request(usuario)

    if not Usuario.valid_pass(request.form['senha']):
        return json_response(message='A senha deve ter pelo menos 6 dígitos', data=[]), 400

    if usuario.login_exists(usuario.cpf, 0):
        return json_response(message='O CPF já está em uso, utilize outro', data=[]), 400

    usuario.senha = Usuario.hash(request.form['senha'])
    identifier = usuario.insert()
    if identifier > 0:
        return json_response(message='Cadastrado realizado!', data=[usuario], redirect=url_for('usuarios.entrar')), 201
    else:
        return json_response(message='Não foi possível cadastrar sua conta', data=[]), 400


@bp_usuarios.route('/sair')
def sair():
    session.pop('user', None)
    session.pop('time', None)
    return redirect(url_for('usuarios.entrar'))

# Rotas da área administrativa
@bp_usuarios.route('/admin/usuarios', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de usuários """
    if Auth().is_allowed('cadastra.usuario'):
        return render_template('admin_lista_usuarios.html')
    else:
        return admin_403_response()


@bp_usuarios.route('/admin/usuarios/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de usuários """
    usuario = Usuario()
    usuario.nivel = Roles.usuario.value
    if Auth().is_allowed('cadastra.usuario', usuario):
        return render_template('admin_form_usuario.html', usuario=usuario)
    else:
        return admin_403_response()


@bp_usuarios.route('/admin/usuarios/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de usuários """
    auth = Auth()
    if auth.is_allowed('cadastra.usuario'):
        usuario = Usuario()
        populate_from_request(usuario)

        if not Usuario.valid_pass(request.form['senha']):
            return json_response(message='A senha deve ter pelo menos 6 dígitos', data=[]), 400

        if usuario.login_exists(usuario.cpf, 0):
            return json_response(message='O CPF já está em uso, utilize outro', data=[]), 400

        usuario.senha = Usuario.hash(request.form['senha'])
        usuario.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if usuario.insert():
            return json_response(message='Usuário cadastrado', data=[usuario], redirect=url_for('usuarios.admin_lista'))
        else:
            return json_response(message='Não foi possível cadastrar o usuário', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_usuarios.route('/admin/usuarios/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de usuários """
    usuario = Usuario()
    usuario.select(identifier)
    if usuario.identifier > 0:
        if Auth().is_allowed('edita.usuario', usuario):
            return render_template('admin_form_usuario.html', usuario=usuario)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_usuarios.route('/admin/usuarios/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de usuários """
    usuario = Usuario()
    usuario.select(identifier)
    if usuario.identifier > 0:
        if Auth().is_allowed('edita.usuario', usuario):
            populate_from_request(usuario)
            # Apenas usuários que podem editar qualquer usuário (e não apenas si mesmo) podem alterar o nível de perm.
            if Auth().is_allowed('edita.usuario') and 'nivel' in request.form:
                usuario.nivel = int(request.form['nivel'])

            if usuario.login_exists(usuario.cpf, usuario.identifier):
                return json_response(message='O CPF já está em uso, utilize outro', data=[]), 400

            # Altera senha apenas se for enviado um valor novo
            if 'senha' in request.form and len(request.form['senha']) > 0:
                if not Usuario.valid_pass(request.form['senha']):
                    return json_response(message='A senha deve ter pelo menos 6 dígitos', data=[]), 400
                else:
                    usuario.senha = Usuario.hash(request.form['senha'])
                    usuario.update_password()

            usuario.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if usuario.update():
                return json_response(message='Usuário atualizado!', data=[usuario])
            else:
                return json_response(message='Não foi possível editar o usuário', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Usuário não encontrado', data=[]), 404


@bp_usuarios.route('/admin/usuarios/busca')
@logado
def admin_busca():
    usuario = Usuario()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    resultados = usuario.search(busca, inicio, fim)
    total = usuario.total()
    filtrado = usuario.count(busca)
    return data_tables_response(draw, total, filtrado, resultados)


@bp_usuarios.route('/admin/usuarios/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    usuario = Usuario()
    usuario.select(identifier)
    if usuario.identifier > 0:
        if Auth().is_allowed('remove.usuario', usuario):
            if usuario.delete():
                return json_response(message='Usuário removido!', data=[])
            else:
                return json_response(message='Não foi possível remover o usuário', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Usuário não encontrado', data=[]), 404


def populate_from_request(usuario: Usuario):
    # Atribui valores do post ao model
    usuario.nome = request.form['nome']
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
    usuario.cpf = request.form['cpf']
