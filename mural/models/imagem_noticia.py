from mural.models import Noticia, Usuario
from mural.models.base import BaseModel, DataBase


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

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO imagem_noticia 
                        (noticiaid, lengenda, imagem, ordem, data_cadastro, data_atualizacao)
                        VALUES 
                        (%s, %s, %s, %s, %s, %s)""", (self.noticia_id, self.legenda, self.imagem, self.ordem,
                                                      self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        new_id = c.lastrowid
        c.close()
        return new_id

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
        for (row, key) in c:
            list_all[key] = ImagemNoticia()
            list_all[key].identifier = row[0]
            list_all[key].noticia_id = row[1]
            list_all[key].legenda = row[2]
            list_all[key].imagem = row[3]
            list_all[key].ordem = row[4]
            list_all[key].data_cadastro = row[5]
            list_all[key].data_atualizacao = row[6]
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
        c.execute("ALTER TABLE `imagem_noticia` ADD FOREIGN KEY (`noticiaid`) REFERENCES `noticia` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()
