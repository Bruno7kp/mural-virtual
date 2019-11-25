# coding: utf-8
from flask import Blueprint, render_template, request

from mural.mod_base.auth import logado
from mural.mod_base.base_model import data_tables_response
from mural.mod_logs import Logs

bp_logs = Blueprint('logs', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública


# Rotas da área administrativa
@bp_logs.route('/admin/logs')
@logado
def admin_lista():
    return render_template('admin_lista_logs.html')


@bp_logs.route('/admin/logs/busca')
@logado
def admin_busca():
    logs = Logs()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    resultados = logs.search(busca, inicio, fim)
    total = logs.total()
    filtrado = logs.count(busca)
    return data_tables_response(draw, total, filtrado, resultados)
