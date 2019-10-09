from mural.models import Anuncio, Usuario
from mural.models.base import BaseModel, DataBase


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
        for (row, key) in c:
            list_all[key] = ImagemAnuncio()
            list_all[key].identifier = row[0]
            list_all[key].anuncio_id = row[1]
            list_all[key].legenda = row[2]
            list_all[key].imagem = row[3]
            list_all[key].ordem = row[4]
            list_all[key].data_cadastro = row[5]
            list_all[key].data_atualizacao = row[6]
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
        c.execute("ALTER TABLE `imagem_anuncio` ADD FOREIGN KEY (`anuncioid`) REFERENCES `anuncio` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()
