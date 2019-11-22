# coding: utf-8
from datetime import timedelta

from flask import Flask, redirect, url_for, render_template
from mural import bp_home, bp_avisos, bp_noticias, bp_anuncios, bp_dashboard, bp_banner, bp_universidade, bp_usuarios, \
    bp_logs
from mural.mod_base.auth import SESSION_LIMIT, Auth

app = Flask(__name__, template_folder='mural/templates', static_url_path='/static', static_folder='mural/static')

app.secret_key = b'_8#y2P"g8l1x\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=SESSION_LIMIT)


@app.context_processor
def inject_auth():
    return dict(auth=Auth())


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
