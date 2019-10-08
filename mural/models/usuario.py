from mural.models.base import BaseModel, DataBase


class Usuario(BaseModel):
    def __init__(self, identifier=0, nome="", email="", telefone="", cpf="", senha="", nivel=None, data_cadastro="",
                 data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cpf = cpf
        self.senha = senha
        self.nivel = nivel
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def insert(self):
        c = self.db.con.cursor()
        c.execute("""INSERT INTO usuario 
                    (nome, email, telefone, cpf, senha, nivel, data_cadastro, data_atualizacao)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s)""", (self.nome, self.email, self.telefone, self.cpf, self.senha,
                                                          self.nivel, self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        new_id = c.lastrowid
        c.close()
        return new_id

    def update(self):
        c = self.db.con.cursor()
        c.execute("""UPDATE usuario 
                SET nome = %s, email = %s, telefone = %s, cpf = %s, senha = %s, nivel = %s, data_cadastro = %s, 
                data_atualizacao = %s WHERE id = %s""", (self.nome, self.email, self.telefone, self.cpf, self.senha,
                                                         self.nivel, self.data_cadastro, self.data_atualizacao,
                                                         self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self):
        c = self.db.con.cursor()
        c.execute("""DELETE FROM usuario WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, nome, email, telefone, cpf, senha, nivel, data_cadastro, data_atualizacao 
                FROM usuario WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.nome = row[1]
            self.email = row[2]
            self.telefone = row[3]
            self.cpf = row[4]
            self.senha = row[5]
            self.nivel = row[6]
            self.data_cadastro = row[7]
            self.data_atualizacao = row[8]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, nome, email, telefone, cpf, senha, nivel, data_cadastro, data_atualizacao 
                FROM usuario ORDER BY nome""")
        list_all = []
        for (row, key) in c:
            list_all[key] = Usuario()
            list_all[key].identifier = row[0]
            list_all[key].nome = row[1]
            list_all[key].email = row[2]
            list_all[key].telefone = row[3]
            list_all[key].cpf = row[4]
            list_all[key].senha = row[5]
            list_all[key].nivel = row[6]
            list_all[key].data_cadastro = row[7]
            list_all[key].data_atualizacao = row[8]
        c.close()
        return list_all

    @staticmethod
    def create_table():
        db = DataBase()
        c = db.con.cursor()
        c.execute("""CREATE TABLE `usuario` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `nome` varchar(255),
          `email` varchar(255),
          `telefone` varchar(255),
          `cpf` varchar(255),
          `senha` varchar(255),
          `nivel` int,
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
