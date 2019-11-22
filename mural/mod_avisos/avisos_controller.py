# coding: utf-8
from flask import Blueprint, render_template, request

from mural.mod_avisos import Aviso
from mural.mod_base.auth import logado
from mural.mod_base.base_model import json_response, data_tables_response

bp_avisos = Blueprint('avisos', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_avisos.route('/avisos')
def avisos():
    return render_template('formAvisos.html')

# Rotas da área administrativa
@bp_avisos.route('/admin/avisos')
@logado
def admin_lista():
    return render_template('admin_lista_avisos.html')


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


