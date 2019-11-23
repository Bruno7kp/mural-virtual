# coding: utf-8
import datetime

from flask import Blueprint, render_template, request, url_for

from mural.mod_base.auth import logado, Auth
from mural.mod_base.base_model import data_tables_response, json_response, admin_404_response, admin_403_response
from mural.mod_noticias import Noticia

bp_noticias = Blueprint('noticias', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_noticias.route('/noticias')
def noticias():
    return render_template("listNoticias.html")

# Rotas da área administrativa
@bp_noticias.route('/admin/noticias', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de notícias """
    if Auth().is_allowed('cadastra.noticia'):
        return render_template('admin_lista_noticias.html')
    else:
        return admin_403_response()


@bp_noticias.route('/admin/noticias/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de notpicias """
    noticia = Noticia()
    if Auth().is_allowed('edita.noticia', noticia):
        return render_template('admin_form_noticias.html', noticia=noticia)
    else:
        return admin_403_response()


@bp_noticias.route('/admin/noticias/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de notícias """
    auth = Auth()
    if auth.is_allowed('cadastra.noticia'):
        noticia = Noticia()
        populate_from_request(noticia)
        noticia.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        noticia.usuario_id = auth.user.identifier
        if noticia.insert():
            return json_response(message='Notícia cadastrada', data=[noticia], redirect=url_for('noticias.admin_lista'))
        else:
            return json_response(message='Não foi possível cadastrar a notícia', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_noticias.route('/admin/noticias/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de notícias """
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('edita.noticia', noticia):
            return render_template('admin_form_noticias.html', noticia=noticia)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_noticias.route('/admin/noticias/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de notícias """
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('edita.noticia', noticia):
            populate_from_request(noticia)
            noticia.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if noticia.update():
                return json_response(message='Notícia atualizada!', data=[noticia]), 200
            else:
                return json_response(message='Não foi possível editar a notícia', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Notícia não encontrada', data=[]), 404


@bp_noticias.route('/admin/noticias/busca')
@logado
def admin_busca():
    noticia = Noticia()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    resultados = noticia.search(busca, inicio, fim)
    total = noticia.total()
    filtrado = noticia.count(busca)
    return data_tables_response(draw, total, filtrado, resultados)


@bp_noticias.route('/admin/noticias/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('remove.noticia', noticia):
            if noticia.delete():
                return json_response(message='Notícia removida!', data=[]), 200
            else:
                return json_response(message='Não foi possível remover a notícia', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Notícia não encontrada', data=[]), 404


def populate_from_request(noticia: Noticia):
    # Atribui valores do post ao model
    noticia.titulo = request.form['titulo']
    noticia.data_entrada = request.form['data_entrada']
    noticia.data_saida = request.form['data_saida']
    noticia.conteudo = request.form['conteudo']
