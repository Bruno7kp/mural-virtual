from mural.models import Usuario
from mural.models.base import BaseModel, DataBase


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

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO noticia 
                    (usuario_id, titulo, conteudo, data_entrada, data_saida, data_cadastro, data_atualizacao)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.titulo, self.conteudo, self.data_entrada,
                                                      self.data_saida, self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        new_id = c.lastrowid
        c.close()
        return new_id

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
        c.execute("""SELECT id, usuario_id, titulo, conteudo, data_entrada, data_saida, data_cadastro, data_atualizacao 
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
        c.execute("""SELECT id, usuario_id, titulo, conteudo, data_entrada, data_saida, data_cadastro, data_atualizacao
                FROM noticia ORDER BY data_entrada DESC""")
        list_all = []
        for (row, key) in c:
            list_all[key] = Noticia()
            list_all[key].identifier = row[0]
            list_all[key].usuario_id = row[1]
            list_all[key].titulo = row[2]
            list_all[key].conteudo = row[3]
            list_all[key].data_entrada = row[4]
            list_all[key].data_saida = row[5]
            list_all[key].data_cadastro = row[6]
            list_all[key].data_atualizacao = row[7]
        c.close()
        return list_all

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
