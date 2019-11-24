# coding: utf-8
import datetime

from flask import Blueprint, render_template, request, url_for

from mural.mod_avisos import Aviso
from mural.mod_base.auth import logado, Auth
from mural.mod_base.base_model import json_response, data_tables_response, admin_403_response, admin_404_response

bp_avisos = Blueprint('avisos', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_avisos.route('/avisos')
def avisos():
    return render_template("listAvisos.html")

# Rotas da área administrativa
@bp_avisos.route('/admin/avisos', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de avisos """
    if Auth().is_allowed('cadastra.aviso'):
        return render_template('admin_lista_avisos.html')
    else:
        return admin_403_response()


@bp_avisos.route('/admin/avisos/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de avisos """
    aviso = Aviso()
    if Auth().is_allowed('cadastra.aviso', aviso):
        return render_template('admin_form_aviso.html', aviso=aviso)
    else:
        return admin_403_response()


@bp_avisos.route('/admin/avisos/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de avisos """
    auth = Auth()
    if auth.is_allowed('cadastra.aviso'):
        aviso = Aviso()
        populate_from_request(aviso)
        aviso.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        aviso.usuario_id = auth.user.identifier
        if aviso.insert():
            return json_response(message='Aviso cadastrado!', data=[aviso], redirect=url_for('avisos.admin_lista'))
        else:
            return json_response(message='Não foi possível cadastrar o aviso', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_avisos.route('/admin/avisos/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de avisos """
    aviso = Aviso()
    aviso.select(identifier)
    if aviso.identifier > 0:
        if Auth().is_allowed('edita.aviso', aviso):
            return render_template('admin_form_aviso.html', aviso=aviso)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_avisos.route('/admin/avisos/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de avisos """
    aviso = Aviso()
    aviso.select(identifier)
    if aviso.identifier > 0:
        if Auth().is_allowed('edita.aviso', aviso):
            populate_from_request(aviso)
            aviso.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if aviso.update():
                return json_response(message='Aviso atualizado!', data=[aviso])
            else:
                return json_response(message='Não foi possível editar o aviso', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Aviso não encontrado', data=[]), 404


@bp_avisos.route('/admin/avisos/busca')
@logado
def admin_busca():
    aviso = Aviso()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    resultados = aviso.search(busca, inicio, fim)
    total = aviso.total()
    filtrado = aviso.count(busca)
    return data_tables_response(draw, total, filtrado, resultados)


@bp_avisos.route('/admin/avisos/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    aviso = Aviso()
    aviso.select(identifier)
    if aviso.identifier > 0:
        if Auth().is_allowed('remove.aviso', aviso):
            if aviso.delete():
                return json_response(message='Aviso removido!', data=[])
            else:
                return json_response(message='Não foi possível remover o aviso', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Aviso não encontrado', data=[]), 404


def populate_from_request(aviso: Aviso):
    # Atribui valores do post ao model
    aviso.titulo = request.form['titulo']
    aviso.data_entrada = request.form['data_entrada']
    aviso.data_saida = request.form['data_saida']
    aviso.conteudo = request.form['conteudo']
