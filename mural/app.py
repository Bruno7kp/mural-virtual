# coding: utf-8

from flask import Flask, redirect, url_for, render_template
from mod_home.home import bp_home
from mod_noticias.noticias import bp_noticias
from mod_avisos.avisos import bp_avisos
from mod_anuncios.anuncios import bp_anuncios
from mod_dashboard.dashboard import bp_dashboard

app = Flask(__name__)

app.register_blueprint(bp_home)
app.register_blueprint(bp_noticias)
app.register_blueprint(bp_avisos)
app.register_blueprint(bp_anuncios)
app.register_blueprint(bp_dashboard)

if __name__ == '__main__':
    app.run()
