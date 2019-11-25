# coding: utf-8
from flask import Blueprint, render_template

from mural.mod_anuncios import Anuncio
from mural.mod_avisos import Aviso
from mural.mod_banner import Banner
from mural.mod_base.auth import logado
from mural.mod_noticias import Noticia

bp_home = Blueprint('home', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_home.route('/')
def home():
    aviso = Aviso()
    avisos = aviso.search('%%', 0, 10, True)
    anuncio = Anuncio()
    anuncios = anuncio.search('%%', 0, 5, 1, 0, True)
    noticia = Noticia()
    noticias = noticia.search('%%', 0, 10, True)
    banner = Banner()
    banners = banner.all()
    return render_template('home.html', avisos=avisos, anuncios=anuncios, noticias=noticias, banners=banners)

# Rotas da área administrativa
@bp_home.route('/admin')
@logado
def admin_home():
    anuncio = Anuncio()
    pendente = anuncio.count('%%', 0, 0, False)
    return render_template('admin_home.html', pendente=pendente)
