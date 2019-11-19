# coding: utf-8
from flask import Blueprint, render_template, request

from mural.mod_base.base_model import data_tables_response
from mural.mod_noticias import Noticia

bp_noticias = Blueprint('noticias', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_noticias.route("/noticias")
def noticias():
    return render_template("formNoticias.html")

# Rotas da área administrativa
@bp_noticias.route("/admin/noticias")
def admin_lista():
    return render_template("admin_lista_noticias.html")


@bp_noticias.route('/admin/noticias/busca')
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
