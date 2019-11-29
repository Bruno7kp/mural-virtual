import datetime

from mural.mod_base.base_model import show_date
from mural.mod_usuarios import Usuario
from mural.mod_base import BaseModel, DataBase


class Logs(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, acao="", tabela_relacionada="", id_relacionado=0, data_cadastro="",
                 data_atualizacao=None):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.acao = acao
        self.tabela_relacionada = tabela_relacionada
        self.id_relacionado = id_relacionado
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def serialize(self):
        return {
            'id': self.identifier,
            'usuario_id': self.usuario_id,
            'acao': self.acao,
            'tabela_relacionada': self.tabela_relacionada,
            'id_relacionado': self.id_relacionado,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        return [
            self.acao,
            show_date(self.data_cadastro)
        ]

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO logs 
            (usuario_id, acao, tabela_relacionada, id_relacionado, data_cadastro, data_atualizacao)
            VALUES 
            (%s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.acao, self.tabela_relacionada, self.id_relacionado,
                                          self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE logs 
        SET usuario_id = %s, acao = %s, tabela_relacionada = %s, id_relacionado = %s, data_cadastro = %s, 
        data_atualizacao = %s WHERE id = %s""", (self.usuario_id, self.acao, self.tabela_relacionada,
                                                 self.id_relacionado, self.data_cadastro, self.data_atualizacao,
                                                 self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM logs WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, acao, tabela_relacionada, id_relacionado, data_cadastro, data_atualizacao 
        FROM logs WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.usuario_id = row[1]
            self.acao = row[2]
            self.tabela_relacionada = row[3]
            self.id_relacionado = row[4]
            self.data_cadastro = row[5]
            self.data_atualizacao = row[6]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, acao, tabela_relacionada, id_relacionado, data_cadastro, data_atualizacao 
        FROM logs ORDER BY data_cadastro DESC""")
        list_all = []
        for row in c:
            log = Logs()
            log.identifier = row[0]
            log.usuario_id = row[1]
            log.acao = row[2]
            log.tabela_relacionada = row[3]
            log.id_relacionado = row[4]
            log.data_cadastro = row[5]
            log.data_atualizacao = row[6]
            list_all.append(log)
        c.close()
        return list_all

    def search(self, text: str, start: int, limit: int):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, acao, tabela_relacionada, id_relacionado, 
                    DATE_FORMAT(data_cadastro, '%%Y-%%m-%%dT%%H:%%i'), data_atualizacao FROM logs WHERE acao LIKE %s 
                    ORDER BY data_cadastro DESC LIMIT %s, %s""",
                  (text, start, limit))
        list_all = []
        for row in c:
            log = Logs()
            log.identifier = row[0]
            log.usuario_id = row[1]
            log.acao = row[2]
            log.tabela_relacionada = row[3]
            log.id_relacionado = row[4]
            log.data_cadastro = row[5]
            log.data_atualizacao = row[6]
            list_all.append(log)
        c.close()
        return list_all

    def total(self):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM logs")
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def count(self, text):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM logs WHERE acao LIKE %s", text)
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

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
        c.execute("""CREATE TABLE `logs` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `usuario_id` int,
          `acao` varchar(255),
          `tabela_relacionada` varchar(255),
          `id_relacionado` int,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `logs` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        db = DataBase()
        c = db.con.cursor()
        # Inserir na tabela
        db.con.commit()
        c.close()
