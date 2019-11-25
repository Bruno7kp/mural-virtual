import datetime

from flask import url_for

from mural.mod_base.base_model import show_date
from mural.mod_usuarios import Usuario
from mural.mod_base import BaseModel, DataBase


class Noticia(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, titulo="", conteudo="", data_entrada="", data_saida="",
                 data_cadastro="", data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def serialize(self):
        return {
            'id': self.identifier,
            'usuario_id': self.usuario_id,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'data_entrada': self.data_entrada,
            'data_saida': self.data_saida,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        return [
            self.identifier,
            self.titulo,
            show_date(self.data_entrada),
            show_date(self.data_saida),
            '<a href="' + url_for('noticias.admin_edicao', identifier=self.identifier) +
            '" class="btn btn-warning btn-sm"><i class="fa fa-pen fa-fw fa-sm text-white-50"></i> Editar</a> ' +
            '<button data-delete="' + url_for('noticias.admin_remover', identifier=self.identifier) +
            '" class="btn btn-danger btn-sm"><i class="fa fa-trash fa-fw fa-sm text-white-50"></i> Remover</button>'
        ]

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO noticia 
                    (usuario_id, titulo, conteudo, data_entrada, data_saida, data_cadastro, data_atualizacao)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.titulo, self.conteudo, self.data_entrada,
                                                      self.data_saida, self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE noticia 
                SET usuario_id = %s, titulo = %s, conteudo = %s, data_entrada = %s, data_saida = %s, data_cadastro = %s, 
                data_atualizacao = %s WHERE id = %s""", (self.usuario_id, self.titulo, self.conteudo, self.data_entrada,
                                                         self.data_saida, self.data_cadastro, self.data_atualizacao,
                                                         self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM noticia WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, titulo, conteudo, DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao 
                        FROM noticia WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.usuario_id = row[1]
            self.titulo = row[2]
            self.conteudo = row[3]
            self.data_entrada = row[4]
            self.data_saida = row[5]
            self.data_cadastro = row[6]
            self.data_atualizacao = row[7]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, titulo, conteudo, DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao
                        FROM noticia ORDER BY data_entrada DESC""")
        list_all = []
        for row in c:
            noticia = Noticia()
            noticia.identifier = row[0]
            noticia.usuario_id = row[1]
            noticia.titulo = row[2]
            noticia.conteudo = row[3]
            noticia.data_entrada = row[4]
            noticia.data_saida = row[5]
            noticia.data_cadastro = row[6]
            noticia.data_atualizacao = row[7]
            list_all.append(noticia)
        c.close()
        return list_all

    def search(self, text: str, start: int, limit: int, filter_date: bool = False):
        c = self.db.con.cursor()
        if filter_date:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""SELECT id, usuario_id, titulo, conteudo, DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                                    DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao
                                    FROM noticia WHERE titulo LIKE %s AND %s >= data_entrada AND %s < data_saida 
                                    ORDER BY data_entrada DESC LIMIT %s, %s""",
                      (text, now, now, start, limit))
        else:
            c.execute("""SELECT id, usuario_id, titulo, conteudo, DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao
                        FROM noticia WHERE titulo LIKE %s ORDER BY data_entrada DESC LIMIT %s, %s""",
                      (text, start, limit))
        list_all = []
        for row in c:
            noticia = Noticia()
            noticia.identifier = row[0]
            noticia.usuario_id = row[1]
            noticia.titulo = row[2]
            noticia.conteudo = row[3]
            noticia.data_entrada = row[4]
            noticia.data_saida = row[5]
            noticia.data_cadastro = row[6]
            noticia.data_atualizacao = row[7]
            list_all.append(noticia)
        c.close()
        return list_all

    def total(self):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM noticia")
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def count(self, text, filter_date: bool = False):
        c = self.db.con.cursor()
        if filter_date:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("SELECT COUNT(id) AS total FROM noticia WHERE titulo LIKE %s AND (%s >= data_entrada AND %s < data_saida)",
                      (text, now, now))
        else:
            c.execute("SELECT COUNT(id) AS total FROM noticia WHERE titulo LIKE %s", text)
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def get_cover(self):
        imagem = ImagemNoticia()
        imagens = imagem.select_by_parent(self.identifier)
        if len(imagens) > 0:
            return imagens[0].imagem
        return ''

    def get_images(self):
        imagem = ImagemNoticia()
        imagens = imagem.select_by_parent(self.identifier)
        return imagens

    @staticmethod
    def has_ownership() -> bool:
        return True

    def get_owner_id(self) -> int:
        return self.usuario_id

    def get_owner(self) -> Usuario:
        usuario = Usuario()
        usuario.select(self.get_owner_id())
        return usuario

    @staticmethod
    def create_table():
        db = DataBase()
        c = db.con.cursor()
        c.execute("""CREATE TABLE `noticia` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `usuario_id` int,
          `titulo` varchar(255),
          `conteudo` text,
          `data_entrada` datetime,
          `data_saida` datetime,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `noticia` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()


class ImagemNoticia(BaseModel):
    def __init__(self, identifier=0, noticia_id=0, legenda="", imagem="", ordem=0, data_cadastro="",
                 data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.noticia_id = noticia_id
        self.legenda = legenda
        self.imagem = imagem
        self.ordem = ordem
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def serialize(self):
        if not isinstance(self.imagem, str):
            self.imagem = self.imagem.decode('utf-8')
        return {
            'id': self.identifier,
            'noticia_id': self.noticia_id,
            'legenda': self.legenda,
            'imagem': self.imagem,
            'ordem': self.ordem,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        return []

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO imagem_noticia 
                        (noticiaid, lengenda, imagem, ordem, data_cadastro, data_atualizacao)
                        VALUES 
                        (%s, %s, %s, %s, %s, %s)""", (self.noticia_id, self.legenda, self.imagem, self.ordem,
                                                      self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE imagem_noticia 
            SET noticiaid = %s, lengenda = %s, imagem = %s, ordem = %s, data_cadastro = %s, data_atualizacao = %s 
            WHERE id = %s""", (self.noticia_id, self.legenda, self.imagem, self.ordem, self.data_cadastro,
                               self.data_atualizacao, self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM imagem_noticia WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, noticiaid, lengenda, imagem, ordem, data_cadastro, data_atualizacao 
                            FROM imagem_noticia WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.noticia_id = row[1]
            self.legenda = row[2]
            self.imagem = row[3]
            self.ordem = row[4]
            self.data_cadastro = row[5]
            self.data_atualizacao = row[6]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, noticiaid, lengenda, imagem, ordem, data_cadastro, data_atualizacao
                    FROM imagem_noticia ORDER BY ordem""")
        list_all = []
        for row in c:
            imagem = ImagemNoticia()
            imagem.identifier = row[0]
            imagem.noticia_id = row[1]
            imagem.legenda = row[2]
            imagem.imagem = row[3]
            imagem.ordem = row[4]
            imagem.data_cadastro = row[5]
            imagem.data_atualizacao = row[6]
            list_all.append(imagem)
        c.close()
        return list_all

    def select_by_parent(self, identifier: int):
        c = self.db.con.cursor()
        c.execute("""SELECT id, noticiaid, lengenda, imagem, ordem, data_cadastro, data_atualizacao
                    FROM imagem_noticia WHERE noticiaid = %s ORDER BY ordem""", identifier)
        list_all = []
        for row in c:
            imagem = ImagemNoticia()
            imagem.identifier = row[0]
            imagem.noticia_id = row[1]
            imagem.legenda = row[2]
            imagem.imagem = row[3]
            imagem.ordem = row[4]
            imagem.data_cadastro = row[5]
            imagem.data_atualizacao = row[6]
            list_all.append(imagem)
        c.close()
        return list_all

    def get_parent(self) -> Noticia:
        noticia = Noticia()
        noticia.select(self.noticia_id)
        return noticia

    @staticmethod
    def has_ownership() -> bool:
        return True

    def get_owner_id(self) -> int:
        return self.get_parent().usuario_id

    def get_owner(self) -> Usuario:
        usuario = Usuario()
        usuario.select(self.get_owner_id())
        return usuario

    @staticmethod
    def create_table():
        db = DataBase()
        c = db.con.cursor()
        c.execute("""CREATE TABLE `imagem_noticia` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `noticiaid` int,
          `lengenda` varchar(255),
          `imagem` longblob,
          `ordem` int,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `imagem_noticia` ADD FOREIGN KEY (`noticiaid`) REFERENCES `noticia` (`id`) ON DELETE CASCADE;")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()
