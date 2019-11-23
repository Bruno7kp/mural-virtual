import pymysql
import re
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from mural.mod_usuarios import Usuario
from mural.mod_avisos import Aviso
from mural.mod_noticias import Noticia, ImagemNoticia
from mural.mod_anuncios import Anuncio, ImagemAnuncio
from mural.mod_universidade import Universidade
from mural.mod_banner import Banner
from mural.mod_logs import Logs


def create_database():
    con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, charset='utf8mb4')
    if re.match("^[A-Za-z0-9_]*$", DB_NAME):
        c = con.cursor()
        c.execute('CREATE database ' + DB_NAME)
        con.commit()
        c.close()
    else:
        print('Nome de banco de dados inválido')


def migrate_database():
    # Cria tabelas
    Usuario.create_table()
    Aviso.create_table()
    Noticia.create_table()
    ImagemNoticia.create_table()
    Anuncio.create_table()
    ImagemAnuncio.create_table()
    Universidade.create_table()
    Banner.create_table()
    Logs.create_table()
    # Adiciona usuários e dados da universidade
    Usuario.insert_dummy()
    Universidade.insert_dummy()
