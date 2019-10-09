from mural.models import Usuario
from mural.models.base import BaseModel, DataBase


class Banner(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, redireciona_url="", imagem="", ordem=0, data_cadastro="",
                 data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.redireciona_url = redireciona_url
        self.imagem = imagem
        self.ordem = ordem
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO banner 
                (usuario_id, redireciona_url, imagem, ordem, data_cadastro, data_atualizacao)
                VALUES 
                (%s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.redireciona_url, self.imagem, self.ordem,
                                              self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE banner 
                    SET usuario_id = %s, redireciona_url = %s, imagem = %s, ordem = %s, data_cadastro = %s, 
                    data_atualizacao = %s WHERE id = %s""", (self.usuario_id, self.redireciona_url, self.imagem,
                                                             self.ordem, self.data_cadastro, self.data_atualizacao,
                                                             self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM banner WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, redireciona_url, imagem, ordem, data_cadastro, data_atualizacao 
                    FROM banner WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.usuario_id = row[1]
            self.redireciona_url = row[2]
            self.imagem = row[3]
            self.ordem = row[4]
            self.data_cadastro = row[5]
            self.data_atualizacao = row[6]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, redireciona_url, imagem, ordem, data_cadastro, data_atualizacao
                                FROM banner ORDER BY ordem""")
        list_all = []
        for (row, key) in c:
            list_all[key] = Banner()
            list_all[key].identifier = row[0]
            list_all[key].usuario_id = row[1]
            list_all[key].redireciona_url = row[2]
            list_all[key].imagem = row[3]
            list_all[key].ordem = row[4]
            list_all[key].data_cadastro = row[5]
            list_all[key].data_atualizacao = row[6]
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
        c.execute("""CREATE TABLE `banner` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `usuario_id` int,
          `redireciona_url` varchar(255),
          `imagem` longblob,
          `ordem` int,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `banner` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()
