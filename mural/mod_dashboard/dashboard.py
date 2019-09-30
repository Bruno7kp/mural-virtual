# coding: utf-8
from flask import Blueprint, render_template

bp_dashboard = Blueprint('dashboard', __name__, url_prefix='/', template_folder='templates')

@bp_dashboard.route("/dashboard")
def dashboard():
    return render_template("formDashboard.html")