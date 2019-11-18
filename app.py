# coding: utf-8

from flask import Flask, redirect, url_for, render_template
from mural import bp_home, bp_avisos, bp_noticias, bp_anuncios, bp_dashboard, bp_banner, bp_universidade, bp_usuarios, \
    bp_logs

app = Flask(__name__, template_folder='mural/templates', static_url_path='/static', static_folder='mural/static')

app.register_blueprint(bp_home)
app.register_blueprint(bp_noticias)
app.register_blueprint(bp_avisos)
app.register_blueprint(bp_anuncios)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_banner)
app.register_blueprint(bp_universidade)
app.register_blueprint(bp_usuarios)
app.register_blueprint(bp_logs)

if __name__ == '__main__':
    app.run()
