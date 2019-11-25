import datetime

from flask import url_for

from mural.mod_base.base_model import show_date
from mural.mod_usuarios import Usuario
from mural.mod_base import BaseModel, DataBase, Auth


class Anuncio(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, titulo="", conteudo="", aprovado=False, data_entrada="",
                 data_saida="", data_cadastro="", data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo = conteudo
        self.aprovado = aprovado
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
            'aprovado': self.aprovado,
            'data_entrada': self.data_entrada,
            'data_saida': self.data_saida,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        edit = ''
        remove = ''
        auth = Auth()
        if auth.is_allowed('edita.anuncio', self):
            edit = '<a href="' + url_for('anuncios.admin_edicao', identifier=self.identifier) + '" class="btn btn-warning btn-sm"><i class="fa fa-pen fa-fw fa-sm text-white-50"></i> Editar</a> '
        if auth.is_allowed('remove.anuncio', self):
            remove = '<button data-delete="' + url_for('anuncios.admin_remover', identifier=self.identifier) + '" class="btn btn-danger btn-sm"><i class="fa fa-trash fa-fw fa-sm text-white-50"></i> Remover</button>'
        status = '<span class="badge badge-warning">Aprovação pendente</span>'
        if self.aprovado:
            entrada = datetime.datetime.strptime(self.data_entrada, "%Y-%m-%dT%H:%M").timestamp()
            saida = datetime.datetime.strptime(self.data_saida, "%Y-%m-%dT%H:%M").timestamp()
            agora = datetime.datetime.now().timestamp()
            if agora >= entrada and agora < saida:
                status = '<span class="badge badge-success">Disponível</span>'
            else:
                status = '<span class="badge badge-secondary">Expirado</span>'
        usuario = self.get_owner()
        return [
            self.identifier,
            self.titulo,
            status,
            usuario.nome + '<small class="d-block">(' + usuario.cpf + ')</small>',
            show_date(self.data_entrada),
            show_date(self.data_saida),
            edit + remove
        ]

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO anuncio 
            (usuario_id, titulo, conteudo, aprovado, data_entrada, data_saida, data_cadastro, data_atualizacao)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.titulo, self.conteudo, self.aprovado,
                                                  self.data_entrada, self.data_saida, self.data_cadastro,
                                                  self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier > 0

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE anuncio 
        SET usuario_id = %s, titulo = %s, conteudo = %s, aprovado = %s, data_entrada = %s, data_saida = %s, 
        data_cadastro = %s, data_atualizacao = %s WHERE id = %s""", (self. usuario_id, self.titulo, self.conteudo,
                                                                     self.aprovado, self.data_entrada, self.data_saida,
                                                                     self.data_cadastro, self.data_atualizacao,
                                                                     self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows > 0

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM anuncio WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows > 0

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, titulo, conteudo, aprovado,DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                    DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao 
                    FROM anuncio WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.usuario_id = row[1]
            self.titulo = row[2]
            self.conteudo = row[3]
            self.aprovado = int(row[4]) == 1  # transforma em booleano
            self.data_entrada = row[5]
            self.data_saida = row[6]
            self.data_cadastro = row[7]
            self.data_atualizacao = row[8]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, titulo, conteudo, aprovado,DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                    DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao 
                    FROM anuncio ORDER BY data_entrada DESC""")
        list_all = []
        for row in c:
            anuncio = Anuncio()
            anuncio.identifier = row[0]
            anuncio.usuario_id = row[1]
            anuncio.titulo = row[2]
            anuncio.conteudo = row[3]
            anuncio.aprovado = int(row[4]) == 1  # transforma em booleano
            anuncio.data_entrada = row[5]
            anuncio.data_saida = row[6]
            anuncio.data_cadastro = row[7]
            anuncio.data_atualizacao = row[8]
            list_all.append(anuncio)
        c.close()
        return list_all

    def search(self, text: str, start: int, limit: int, approval_filter: int = -1, user_filter: int = 0, filter_date: bool = False):
        c = self.db.con.cursor()
        if filter_date:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""SELECT id, usuario_id, titulo, conteudo, aprovado,DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao 
                                        FROM anuncio WHERE (titulo LIKE %s) AND (%s = -1 OR %s = aprovado) AND
                                        (%s = 0 OR %s = usuario_id) AND (%s >= data_entrada AND %s < data_saida) 
                                        ORDER BY data_entrada DESC LIMIT %s, %s""",
                      (text, approval_filter, approval_filter, user_filter, user_filter, now, now, start, limit))
        else:
            c.execute("""SELECT id, usuario_id, titulo, conteudo, aprovado,DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                            DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao 
                            FROM anuncio WHERE (titulo LIKE %s) AND (%s = -1 OR %s = aprovado) AND
                            (%s = 0 OR %s = usuario_id) ORDER BY data_entrada DESC LIMIT %s, %s""",
                      (text, approval_filter, approval_filter, user_filter, user_filter, start, limit))
        list_all = []
        for row in c:
            anuncio = Anuncio()
            anuncio.identifier = row[0]
            anuncio.usuario_id = row[1]
            anuncio.titulo = row[2]
            anuncio.conteudo = row[3]
            anuncio.aprovado = int(row[4]) == 1  # transforma em booleano
            anuncio.data_entrada = row[5]
            anuncio.data_saida = row[6]
            anuncio.data_cadastro = row[7]
            anuncio.data_atualizacao = row[8]
            list_all.append(anuncio)
        c.close()
        return list_all

    def total(self, approval_filter: int = -1, user_filter: int = 0):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM anuncio WHERE (%s = -1 OR %s = aprovado) AND (%s = 0 OR %s = usuario_id)",
                  (approval_filter, approval_filter, user_filter, user_filter))
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def count(self, text, approval_filter: int = -1, user_filter: int = 0, filter_date: bool = False):
        c = self.db.con.cursor()
        if filter_date:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""SELECT COUNT(id) AS total FROM anuncio WHERE (titulo LIKE %s) AND (%s = -1 OR %s = aprovado) 
                        AND (%s = 0 OR %s = usuario_id) AND (%s >= data_entrada AND %s < data_saida)""",
                      (text, approval_filter, approval_filter, user_filter, user_filter, now, now))
        else:
            c.execute("""SELECT COUNT(id) AS total FROM anuncio WHERE (titulo LIKE %s) AND (%s = -1 OR %s = aprovado) AND
                        (%s = 0 OR %s = usuario_id)""", (text, approval_filter, approval_filter, user_filter, user_filter))
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def get_cover(self):
        imagem = ImagemAnuncio()
        imagens = imagem.select_by_parent(self.identifier)
        if len(imagens) > 0:
            return imagens[0].imagem
        return ''

    def get_images(self):
        imagem = ImagemAnuncio()
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
        c.execute("""CREATE TABLE `anuncio` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `usuario_id` int,
          `titulo` varchar(255),
          `conteudo` text,
          `aprovado` boolean,
          `data_entrada` datetime,
          `data_saida` datetime,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `anuncio` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()


class ImagemAnuncio(BaseModel):
    def __init__(self, identifier=0, anuncio_id=0, legenda="", imagem="", ordem=0, data_cadastro="",
                 data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.anuncio_id = anuncio_id
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
            'anuncio_id': self.anuncio_id,
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
        c.execute("""INSERT INTO imagem_anuncio 
                        (anuncioid, lengenda, imagem, ordem, data_cadastro, data_atualizacao)
                        VALUES 
                        (%s, %s, %s, %s, %s, %s)""", (self.anuncio_id, self.legenda, self.imagem, self.ordem,
                                                      self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE imagem_anuncio 
                            SET anuncioid = %s, lengenda = %s, imagem = %s, ordem = %s, data_cadastro = %s, 
                            data_atualizacao = %s WHERE id = %s""", (self.anuncio_id, self.legenda, self.imagem,
                                                                     self.ordem, self.data_cadastro,
                                                                     self.data_atualizacao,
                                                                     self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM imagem_anuncio WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, anuncioid, lengenda, imagem, ordem, data_cadastro, data_atualizacao 
                            FROM imagem_anuncio WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.anuncio_id = row[1]
            self.legenda = row[2]
            self.imagem = row[3]
            self.ordem = row[4]
            self.data_cadastro = row[5]
            self.data_atualizacao = row[6]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, anuncioid, lengenda, imagem, ordem, data_cadastro, data_atualizacao
                    FROM imagem_anuncio ORDER BY ordem""")
        list_all = []
        for row in c:
            imagem = ImagemAnuncio()
            imagem.identifier = row[0]
            imagem.anuncio_id = row[1]
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
        c.execute("""SELECT id, anuncioid, lengenda, imagem, ordem, data_cadastro, data_atualizacao
                    FROM imagem_anuncio WHERE anuncioid = %s ORDER BY ordem""", identifier)
        list_all = []
        for row in c:
            imagem = ImagemAnuncio()
            imagem.identifier = row[0]
            imagem.anuncio_id = row[1]
            imagem.legenda = row[2]
            imagem.imagem = row[3]
            imagem.ordem = row[4]
            imagem.data_cadastro = row[5]
            imagem.data_atualizacao = row[6]
            list_all.append(imagem)
        c.close()
        return list_all

    def get_parent(self) -> Anuncio:
        noticia = Anuncio()
        noticia.select(self.anuncio_id)
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
        c.execute("""CREATE TABLE `imagem_anuncio` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `anuncioid` int,
          `lengenda` varchar(255),
          `imagem` longblob,
          `ordem` int,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `imagem_anuncio` ADD FOREIGN KEY (`anuncioid`) REFERENCES `anuncio` (`id`) ON DELETE CASCADE;")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()
