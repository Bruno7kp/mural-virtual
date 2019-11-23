import bcrypt as bcrypt
from flask import url_for

from mural.mod_base import BaseModel, DataBase
from mural.mod_base.auth import role_to_str, Roles


class Usuario(BaseModel):
    def __init__(self, identifier=0, nome="", email="", telefone="", cpf="", senha="", nivel=5,
                 data_cadastro="", data_atualizacao=""):
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

    def serialize(self):
        return {
            'identifier': self.identifier,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'nivel': self.nivel,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        return [
            self.identifier,
            self.nome,
            role_to_str(Roles(self.nivel)),
            self.cpf,
            self.email,
            '<a href="' + url_for('usuarios.admin_edicao', identifier=self.identifier) +
            '" class="btn btn-warning btn-sm"><i class="fa fa-pen fa-fw fa-sm text-white-50"></i> Editar</a> ' +
            '<button data-delete="' + url_for('usuarios.admin_remover', identifier=self.identifier) +
            '" class="btn btn-danger btn-sm"><i class="fa fa-trash fa-fw fa-sm text-white-50"></i> Remover</button>'
        ]

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO usuario 
                    (nome, email, telefone, cpf, senha, nivel, data_cadastro, data_atualizacao)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s)""", (self.nome, self.email, self.telefone, self.cpf, self.senha,
                                                          self.nivel, self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE usuario 
                SET nome = %s, email = %s, telefone = %s, cpf = %s, nivel = %s, data_cadastro = %s, 
                data_atualizacao = %s WHERE id = %s""", (self.nome, self.email, self.telefone, self.cpf, self.nivel,
                                                         self.data_cadastro, self.data_atualizacao, self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def update_password(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE usuario
                SET senha = %s WHERE id = %s""", (self.senha, self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
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
            self.populate_from_db(row)
        c.close()
        return self

    def select_by_login(self, login):
        c = self.db.con.cursor()
        c.execute("""SELECT id, nome, email, telefone, cpf, senha, nivel, data_cadastro, data_atualizacao 
                FROM usuario WHERE cpf = %s""", (login,))
        for row in c:
            self.populate_from_db(row)
        c.close()
        return self

    def search(self, text: str, start: int, limit: int):
        c = self.db.con.cursor()
        c.execute("""SELECT id, nome, email, telefone, cpf, senha, nivel, data_cadastro, data_atualizacao 
                FROM usuario WHERE nome LIKE %s OR cpf LIKE %s ORDER BY nome ASC LIMIT %s, %s""",
                  (text, text, start, limit))
        list_all = []
        for row in c:
            usuario = Usuario()
            usuario.identifier = row[0]
            usuario.nome = row[1]
            usuario.email = row[2]
            usuario.telefone = row[3]
            usuario.cpf = row[4]
            usuario.senha = row[5]
            usuario.nivel = row[6]
            usuario.data_cadastro = row[7]
            usuario.data_atualizacao = row[8]
            list_all.append(usuario)
        c.close()
        return list_all

    def total(self):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM usuario")
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def count(self, text):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM usuario WHERE nome LIKE %s OR cpf LIKE %s", (text, text))
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def populate_from_db(self, row):
        self.identifier = row[0]
        self.nome = row[1]
        self.email = row[2]
        self.telefone = row[3]
        self.cpf = row[4]
        self.senha = row[5]
        self.nivel = row[6]
        self.data_cadastro = row[7]
        self.data_atualizacao = row[8]

    def login_exists(self, login, exceptid):
        c = self.db.con.cursor()
        c.execute("""SELECT id FROM usuario WHERE id != %s AND cpf = %s""", (exceptid, login))
        rows = c.rowcount
        c.close()
        return rows > 0

    @staticmethod
    def valid_pass(password):
        return len(password) >= 6

    @staticmethod
    def hash(password):
        return bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_hash(password, hashed):
        return bcrypt.checkpw(bytes(password, encoding='utf-8'), bytes(hashed, encoding='utf-8'))

    def get_role(self):
        return self.nivel

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
    def has_ownership() -> bool:
        return True

    def get_owner_id(self) -> int:
        return self.identifier

    def get_owner(self):
        return self

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
        usuario = Usuario(0, "Fulano da Silva", "fulano@gmail.com", "49 988776655", "000.000.000-00",
                          Usuario.hash("1234"), 4, "2019-01-01", "2019-01-01")
        usuario.insert()
        db.con.commit()
        c.close()
