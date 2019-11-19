# coding: utf-8
from flask import Blueprint, render_template

bp_anuncios = Blueprint('anuncios', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_anuncios.route("/anuncios")
def anuncios():
    return render_template("listAnuncios.html")

# Rotas da área administrativa
