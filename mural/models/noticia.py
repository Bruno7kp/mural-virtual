from mural.models.base import BaseModel, DataBase


class Noticia(BaseModel):
    def __init__(self):
        super().__init__()

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