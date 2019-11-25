import datetime

from flask import url_for

from mural.mod_base.base_model import show_date
from mural.mod_usuarios import Usuario
from mural.mod_base import BaseModel, DataBase


class Aviso(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, titulo="", conteudo="", data_entrada="", data_saida="",
                 data_cadastro="", data_atualizacao=""):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def serialize(self):
        return {
            'id': self.identifier,
            'usuario_id': self.usuario_id,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'data_entrada': self.data_entrada,
            'data_saida': self.data_saida,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        return [
            self.identifier,
            self.titulo,
            show_date(self.data_entrada),
            show_date(self.data_saida),
            '<a href="' + url_for('avisos.admin_edicao', identifier=self.identifier) +
            '" class="btn btn-warning btn-sm"><i class="fa fa-pen fa-fw fa-sm text-white-50"></i> Editar</a> ' +
            '<button data-delete="' + url_for('avisos.admin_remover', identifier=self.identifier) +
            '" class="btn btn-danger btn-sm"><i class="fa fa-trash fa-fw fa-sm text-white-50"></i> Remover</button>'
        ]

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO aviso 
                (usuario_id, titulo, conteudo, data_entrada, data_saida, data_cadastro, data_atualizacao)
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.titulo, self.conteudo, self.data_entrada,
                                                  self.data_saida, self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE aviso 
            SET usuario_id = %s, titulo = %s, conteudo = %s, data_entrada = %s, data_saida = %s, data_cadastro = %s, 
            data_atualizacao = %s WHERE id = %s""", (self.usuario_id, self.titulo, self.conteudo, self.data_entrada,
                                                     self.data_saida, self.data_cadastro, self.data_atualizacao,
                                                     self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM aviso WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, titulo, conteudo, DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao 
                        FROM aviso WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.usuario_id = row[1]
            self.titulo = row[2]
            self.conteudo = row[3]
            self.data_entrada = row[4]
            self.data_saida = row[5]
            self.data_cadastro = row[6]
            self.data_atualizacao = row[7]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, titulo, conteudo, DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao
                        FROM aviso ORDER BY data_entrada DESC""")
        list_all = []
        for row in c:
            aviso = Aviso()
            aviso.identifier = row[0]
            aviso.usuario_id = row[1]
            aviso.titulo = row[2]
            aviso.conteudo = row[3]
            aviso.data_entrada = row[4]
            aviso.data_saida = row[5]
            aviso.data_cadastro = row[6]
            aviso.data_atualizacao = row[7]
            list_all.append(aviso)
        c.close()
        return list_all

    def search(self, text: str, start: int, limit: int, filter_date: bool = False):
        c = self.db.con.cursor()
        if filter_date:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""SELECT id, usuario_id, titulo, conteudo,DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                                    DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao
                                    FROM aviso WHERE titulo LIKE %s AND %s >= data_entrada AND %s < data_saida 
                                    ORDER BY data_entrada DESC LIMIT %s, %s""",
                      (text, now, now, start, limit))
        else:
            c.execute("""SELECT id, usuario_id, titulo, conteudo,DATE_FORMAT(data_entrada, '%%Y-%%m-%%dT%%H:%%i'), 
                        DATE_FORMAT(data_saida, '%%Y-%%m-%%dT%%H:%%i'), data_cadastro, data_atualizacao
                        FROM aviso WHERE titulo LIKE %s ORDER BY data_entrada DESC LIMIT %s, %s""",
                      (text, start, limit))
        list_all = []
        for row in c:
            aviso = Aviso()
            aviso.identifier = row[0]
            aviso.usuario_id = row[1]
            aviso.titulo = row[2]
            aviso.conteudo = row[3]
            aviso.data_entrada = row[4]
            aviso.data_saida = row[5]
            aviso.data_cadastro = row[6]
            aviso.data_atualizacao = row[7]
            list_all.append(aviso)
        c.close()
        return list_all

    def total(self):
        c = self.db.con.cursor()
        c.execute("SELECT COUNT(id) AS total FROM aviso")
        result = c.fetchone()
        number_of_rows = result[0]
        return number_of_rows

    def count(self, text, filter_date: bool = False):
        c = self.db.con.cursor()
        if filter_date:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("SELECT COUNT(id) AS total FROM aviso WHERE titulo LIKE %s AND %s >= data_entrada AND %s < data_saida",
                      (text, now, now))
        else:
            c.execute("SELECT COUNT(id) AS total FROM aviso WHERE titulo LIKE %s", text)
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
        c.execute("""CREATE TABLE `aviso` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `usuario_id` int,
          `titulo` varchar(255),
          `conteudo` text,
          `data_entrada` datetime,
          `data_saida` datetime,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `aviso` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        usuario = Usuario()
        usuario.select_by_login('000.000.000-00')
        if usuario.identifier > 0:
            aviso = Aviso(identifier=0, usuario_id=usuario.identifier, titulo='O Novembro Azul',
                          conteudo="""<p>Em novembro todo mundo se une para conscientização sobre o câncer de próstata: 
                          <strong>O Novembro Azul</strong></p><p>O Centro Especializado em Reabilitação - CER II 
                          Uniplac, juntamento com a Comissão Interna de Prevenção de Acidentes - CIPA Uniplac 2019/2020, 
                          também estão nessa luta.</p><p>E temos a honra de convidar todos os funcionários para o
                          evento <strong>'Novembro Azul na Prevenção do Câncer de Próstata'</strong>, com o Dr.
                          Pedro Schurmann.</p>""", data_entrada='2019-11-01', data_saida='2019-12-31',
                          data_cadastro='2019-11-01', data_atualizacao='2019-11-01')
            aviso.insert()
            aviso = Aviso(identifier=0, usuario_id=usuario.identifier, titulo='Aulas canceladas',
                          conteudo="""<p>Devido ao temporal ocorrido no dia 25/11, informamos que as aulas dos dias 
                          26/11 e 27/11 estão canceladas.</p>""", data_entrada='2019-11-25', data_saida='2019-12-31',
                          data_cadastro='2019-11-25', data_atualizacao='2019-11-25')
            aviso.insert()
            aviso = Aviso(identifier=0, usuario_id=usuario.identifier, titulo='Provas adiadas',
                          conteudo="""<p>Devido ao temporal ocorrido no dia 25/11, informamos que as provas marcadas 
                          para os dias 26/11 e 27/11 serão remarcadas para a próxima semana.</p>""",
                          data_entrada='2019-11-25', data_saida='2019-12-31', data_cadastro='2019-11-25',
                          data_atualizacao='2019-11-25')
            aviso.insert()
            aviso = Aviso(identifier=0, usuario_id=usuario.identifier, titulo='Palestra de TI',
                          conteudo="""<p>Informamos que hávera uma palestra dia 03/12 com a presença do 
                          Bill Gates.</p>""", data_entrada='2019-11-25', data_saida='2019-12-31',
                          data_cadastro='2019-11-25', data_atualizacao='2019-11-25')
            aviso.insert()
            aviso = Aviso(identifier=0, usuario_id=usuario.identifier, titulo='Palestra de Inovação e Empreededorismo',
                          conteudo="""<p>Informamos que hávera uma palestra dia 04/12 com a presença do 
                          Elon Musk.</p>""", data_entrada='2019-11-25', data_saida='2019-12-31',
                          data_cadastro='2019-11-25', data_atualizacao='2019-11-25')
            aviso.insert()

