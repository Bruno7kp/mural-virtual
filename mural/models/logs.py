from mural.models import Usuario
from mural.models.base import BaseModel, DataBase


class Logs(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, acao="", tabela_relacionada="", id_relacionado=0, data_cadastro="",
                 data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.acao = acao
        self.tabela_relacionada = tabela_relacionada
        self.id_relacionado = id_relacionado
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO logs 
            (usuario_id, acao, tabela_relacionada, id_relacionado, data_cadastro, data_atualizacao)
            VALUES 
            (%s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.acao, self.tabela_relacionada, self.id_relacionado,
                                          self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        new_id = c.lastrowid
        c.close()
        return new_id

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
        for (row, key) in c:
            list_all[key] = Logs()
            list_all[key].identifier = row[0]
            list_all[key].usuario_id = row[1]
            list_all[key].acao = row[2]
            list_all[key].tabela_relacionada = row[3]
            list_all[key].id_relacionado = row[4]
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
