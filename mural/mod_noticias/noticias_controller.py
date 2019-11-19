# coding: utf-8
from flask import Blueprint, render_template

bp_noticias = Blueprint('noticias', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_noticias.route("/noticias")
def noticias():
    return render_template("listNoticias.html")

# Rotas da área administrativa
