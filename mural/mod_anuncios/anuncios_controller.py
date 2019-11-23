# coding: utf-8
import datetime

from flask import Blueprint, render_template, request, url_for

from mural.mod_anuncios import Anuncio
from mural.mod_base.auth import logado, Auth
from mural.mod_base.base_model import data_tables_response, admin_403_response, json_response, admin_404_response

bp_anuncios = Blueprint('anuncios', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_anuncios.route('/anuncios')
def anuncios():
    return render_template("listAnuncios.html")

# Rotas da área administrativa
@bp_anuncios.route('/admin/anuncios', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de anúncios """
    if Auth().is_allowed('cadastra.anuncio'):
        return render_template('admin_lista_anuncios.html')
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/aprovacao', methods=['GET'])
@logado
def admin_aprovacao():
    """ Página com listagem de anúncios em aprovação """
    if Auth().is_allowed('edita.anuncio'):
        return render_template('admin_lista_anuncios.html')
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de anúncios """
    anuncio = Anuncio()
    if Auth().is_allowed('cadastra.anuncio', anuncio):
        return render_template('admin_form_anuncio.html', anuncio=anuncio)
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de anúncios """
    auth = Auth()
    if auth.is_allowed('cadastra.anuncio'):
        anuncio = Anuncio()
        populate_from_request(anuncio)
        anuncio.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        anuncio.usuario_id = auth.user.identifier
        # Apenas usuários que podem editar os anúncios já ficam aprovados
        anuncio.aprovado = auth.is_allowed('edita.anuncio')
        if anuncio.insert():
            return json_response(message='Anúncio cadastrado', data=[anuncio], redirect=url_for('anuncios.admin_lista'))
        else:
            return json_response(message='Não foi possível cadastrar o anúncio', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de anúncios """
    anuncio = Anuncio()
    anuncio.select(identifier)
    if anuncio.identifier > 0:
        if Auth().is_allowed('edita.anuncio', anuncio):
            return render_template('admin_form_anuncio.html', anuncio=anuncio)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de anúncios """
    anuncio = Anuncio()
    anuncio.select(identifier)
    if anuncio.identifier > 0:
        if Auth().is_allowed('edita.anuncio', anuncio):
            populate_from_request(anuncio)
            anuncio.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if anuncio.update():
                return json_response(message='Anúncio atualizado!', data=[anuncio]), 200
            else:
                return json_response(message='Não foi possível editar o anúncio', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Anúncio não encontrado', data=[]), 404


@bp_anuncios.route('/admin/anuncios/busca', methods=['GET'])
@logado
def admin_busca():
    """ Busca de anúncios """
    anuncio = Anuncio()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    # Filtra listagem de anúncios para que usuário não possam ver anúncios de outros usuários sem permissão
    auth = Auth()
    if auth.is_allowed('edita.anuncio'):
        resultados = anuncio.search(busca, inicio, fim)
        total = anuncio.total()
        filtrado = anuncio.count(busca)
    else:
        resultados = anuncio.search(busca, inicio, fim, auth.user.identifier)
        total = anuncio.total(auth.user.identifier)
        filtrado = anuncio.count(busca, auth.user.identifier)

    return data_tables_response(draw, total, filtrado, resultados)


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    anuncio = Anuncio()
    anuncio.select(identifier)
    if anuncio.identifier > 0:
        if Auth().is_allowed('remove.anuncio', anuncio):
            if anuncio.delete():
                return json_response(message='Anúncio removido!', data=[]), 200
            else:
                return json_response(message='Não foi possível remover o anúncio', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Anúncio não encontrado', data=[]), 404


def populate_from_request(anuncio: Anuncio):
    # Atribui valores do post ao model
    anuncio.titulo = request.form['titulo']
    anuncio.data_entrada = request.form['data_entrada']
    anuncio.data_saida = request.form['data_saida']
    anuncio.conteudo = request.form['conteudo']
