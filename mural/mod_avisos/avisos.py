# coding: utf-8
from flask import Blueprint, render_template

bp_avisos = Blueprint('avisos', __name__, url_prefix='/', template_folder='templates')

@bp_avisos.route("/avisos")
def avisos():
    return render_template("formAvisos.html")