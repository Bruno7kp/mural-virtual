# coding: utf-8
from flask import Blueprint, render_template

from mural.mod_base.auth import logado

bp_home = Blueprint('home', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_home.route('/')
def home():
    return render_template('home.html')

# Rotas da área administrativa
@bp_home.route('/admin')
@logado
def admin_home():
    return render_template('admin_home.html')
