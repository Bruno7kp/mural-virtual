# coding: utf-8
from flask import Blueprint, render_template

bp_universidade = Blueprint('universidade', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública


# Rotas da área administrativa
@bp_universidade.route("/admin/universidade")
def admin_universidade():
    return render_template("admin_universidade.html")
