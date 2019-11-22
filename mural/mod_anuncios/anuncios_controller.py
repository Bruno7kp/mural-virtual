# coding: utf-8
from flask import Blueprint, render_template, request

from mural.mod_anuncios import Anuncio
from mural.mod_base.auth import logado, Auth, Roles
from mural.mod_base.base_model import data_tables_response, admin_403_response

bp_anuncios = Blueprint('anuncios', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_anuncios.route('/anuncios')
def anuncios():
    return render_template("listAnuncios.html")

# Rotas da área administrativa
@bp_anuncios.route('/admin/anuncios', methods=['GET'])
@logado
def admin_lista():
    return render_template('admin_lista_anuncios.html')


@bp_anuncios.route('/admin/anuncios/aprovacao', methods=['GET'])
@logado
def admin_aprovacao():
    if Auth().is_allowed('edita.anuncio'):
        return render_template('admin_lista_anuncios.html')
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    anuncio = Anuncio()
    return render_template('admin_form_anuncio.html', anuncio=anuncio)


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    anuncio = Anuncio()
    anuncio.select(identifier)
    if Auth().is_allowed('edita.anuncio', anuncio):
        return render_template('admin_form_anuncio.html', anuncio=anuncio)
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/busca', methods=['GET'])
@logado
def admin_busca():
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
