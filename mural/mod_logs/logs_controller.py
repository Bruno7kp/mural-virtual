# coding: utf-8
from flask import Blueprint, render_template

from mural.mod_base.auth import logado

bp_logs = Blueprint('logs', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública


# Rotas da área administrativa
@bp_logs.route('/admin/logs')
@logado
def admin_lista():
    return render_template('admin_lista_logs.html')
