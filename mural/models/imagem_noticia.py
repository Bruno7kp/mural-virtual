from mural.models.base import BaseModel, DataBase


class ImagemNoticia(BaseModel):
    def __init__(self):
        super().__init__()

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
