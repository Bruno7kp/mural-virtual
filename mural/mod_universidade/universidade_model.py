from mural.mod_base import BaseModel, DataBase


class Universidade(BaseModel):
    def __init__(self, identifier=0, nome="", telefone="", email="", logo="", data_cadastro="", data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.logo = logo
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO universidade 
                            (nome, telefone, email, logo, data_cadastro, data_atualizacao)
                            VALUES 
                            (%s, %s, %s, %s, %s, %s)""", (self.nome, self.telefone, self.email, self.logo,
                                                          self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE universidade 
                        SET nome = %s, telefone = %s, email = %s, logo = %s, data_cadastro = %s, data_atualizacao = %s 
                        WHERE id = %s""", (self.nome, self.telefone, self.email, self.logo, self.data_cadastro,
                                           self.data_atualizacao, self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM universidade WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, nome, telefone, email, logo, data_cadastro, data_atualizacao 
                        FROM universidade WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.nome = row[1]
            self.telefone = row[2]
            self.email = row[3]
            self.logo = row[4]
            self.data_cadastro = row[5]
            self.data_atualizacao = row[6]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, nome, telefone, email, logo, data_cadastro, data_atualizacao
                        FROM universidade ORDER BY data_cadastro DESC""")
        list_all = []
        for (row, key) in c:
            list_all[key] = Universidade()
            list_all[key].identifier = row[0]
            list_all[key].nome = row[1]
            list_all[key].telefone = row[2]
            list_all[key].email = row[3]
            list_all[key].logo = row[4]
            list_all[key].data_cadastro = row[5]
            list_all[key].data_atualizacao = row[6]
        c.close()
        return list_all

    @staticmethod
    def has_ownership() -> bool:
        return False

    def get_owner_id(self) -> int:
        return 0

    def get_owner(self) -> None:
        return None

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
