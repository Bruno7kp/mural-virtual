# coding: utf-8
import time

from flask import Blueprint, render_template, request, session, redirect, url_for

from mural.mod_base.auth import logado, Roles
from mural.mod_base.base_model import json_response
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
@bp_usuarios.route('/admin/usuarios')
@logado
def admin_lista():
    return render_template('admin_lista_usuarios.html')


def populate_from_request(usuario: Usuario):
    # Atribui valores do post ao model
    usuario.nome = request.form['nome']
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
    usuario.cpf = request.form['cpf']
    if 'nivel' in request.form:
        usuario.nivel = int(request.form['nivel'])
