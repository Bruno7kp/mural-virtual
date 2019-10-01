# coding: utf-8

from flask import Flask, redirect, url_for, render_template
from mural.mod_home.home import bp_home
from mural.mod_noticias.noticias import bp_noticias
from mural.mod_avisos.avisos import bp_avisos
from mural.mod_anuncios.anuncios import bp_anuncios
from mural.mod_dashboard.dashboard import bp_dashboard

app = Flask(__name__)

app.register_blueprint(bp_home)
app.register_blueprint(bp_noticias)
app.register_blueprint(bp_avisos)
app.register_blueprint(bp_anuncios)
app.register_blueprint(bp_dashboard)

if __name__ == '__main__':
    app.run()
