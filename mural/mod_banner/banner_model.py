from mural.mod_usuarios import Usuario
from mural.mod_base import BaseModel, DataBase


class Banner(BaseModel):
    def __init__(self, identifier=0, usuario_id=0, redireciona_url="", imagem="", ordem=0, data_cadastro="",
                 data_atualizacao=None):
        super().__init__()
        self.identifier = identifier
        self.usuario_id = usuario_id
        self.redireciona_url = redireciona_url
        self.imagem = imagem
        self.ordem = ordem
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao

    def serialize(self):
        return {
            'id': self.identifier,
            'usuario_id': self.usuario_id,
            'redireciona_url': self.redireciona_url,
            'ordem': self.ordem,
            'data_cadastro': self.data_cadastro,
            'data_atualizacao': self.data_atualizacao,
        }

    def serialize_array(self):
        return [
            self.identifier,
            self.usuario_id,
            self.redireciona_url,
            self.imagem,
            self.ordem
        ]

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO banner 
                (usuario_id, redireciona_url, imagem, ordem, data_cadastro, data_atualizacao)
                VALUES 
                (%s, %s, %s, %s, %s, %s)""", (self.usuario_id, self.redireciona_url, self.imagem, self.ordem,
                                              self.data_cadastro, self.data_atualizacao))
        self.db.con.commit()
        self.identifier = c.lastrowid
        c.close()
        return self.identifier

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE banner 
                    SET usuario_id = %s, redireciona_url = %s, imagem = %s, ordem = %s, data_cadastro = %s, 
                    data_atualizacao = %s WHERE id = %s""", (self.usuario_id, self.redireciona_url, self.imagem,
                                                             self.ordem, self.data_cadastro, self.data_atualizacao,
                                                             self.identifier))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM banner WHERE id = %s""", self.identifier)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, identifier):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, redireciona_url, imagem, ordem, data_cadastro, data_atualizacao 
                    FROM banner WHERE id = %s""", identifier)
        for row in c:
            self.identifier = row[0]
            self.usuario_id = row[1]
            self.redireciona_url = row[2]
            self.imagem = row[3]
            self.ordem = row[4]
            self.data_cadastro = row[5]
            self.data_atualizacao = row[6]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id, usuario_id, redireciona_url, imagem, ordem, data_cadastro, data_atualizacao
                                FROM banner ORDER BY ordem""")
        list_all = []
        for row in c:
            banner = Banner()
            banner.identifier = row[0]
            banner.usuario_id = row[1]
            banner.redireciona_url = row[2]
            banner.imagem = row[3]
            banner.ordem = row[4]
            banner.data_cadastro = row[5]
            banner.data_atualizacao = row[6]
            list_all.append(banner)
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
        c.execute("""CREATE TABLE `banner` (
          `id` int PRIMARY KEY AUTO_INCREMENT,
          `usuario_id` int,
          `redireciona_url` varchar(255),
          `imagem` longblob,
          `ordem` int,
          `data_cadastro` datetime,
          `data_atualizacao` datetime
        );""")
        c.execute("ALTER TABLE `banner` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);")
        db.con.commit()
        c.close()

    @staticmethod
    def insert_dummy():
        from mural.mod_base.migration_images import banner_1, banner_2
        usuario = Usuario()
        usuario.select_by_login('000.000.000-00')
        if usuario.identifier > 0:

            banner = Banner(identifier=0, usuario_id=usuario.identifier, redireciona_url='http://novoportal.uniplaclages.edu.br/web/app/Edu/PortalProcessoSeletivo/?c=1&f=1&ct=14#/es/informacoes',
                            imagem=banner_1, ordem=0, data_cadastro='2019-01-01', data_atualizacao='2019-01-01')
            banner.insert()
            banner = Banner(identifier=0, usuario_id=usuario.identifier, redireciona_url='https://paginas.uniplaclages.edu.br/pos-graduacao-2019',
                            imagem=banner_2, data_cadastro='2019-01-01', data_atualizacao='2019-01-01')
            banner.insert()
