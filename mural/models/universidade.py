from mural.models.base import BaseModel, DataBase


class Universidade(BaseModel):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_table():
        db = DataBase()
        c = db.con.cursor()
        c.execute("""CREATE TABLE `universidade` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `nome` varchar(255),
          `telefone` varchar(255),
          `email` varchar(255),
          `logo` longblob,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()