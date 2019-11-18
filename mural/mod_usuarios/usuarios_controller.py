# coding: utf-8
from flask import Blueprint, render_template

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública


# Rotas da área administrativa
@bp_usuarios.route("/admin/usuarios")
def admin_lista():
    return render_template("admin_lista_usuarios.html")
