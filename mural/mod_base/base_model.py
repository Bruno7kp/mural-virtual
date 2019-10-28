import pymysql
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import abc


class DataBase:
    def __init__(self):
        self.con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4')


class BaseModel:
    def __init__(self):
        self.db = DataBase()

    @abc.abstractmethod
    def insert(self) -> int:
        """Insere de uma linha no banco de dados, retorna o id cadastrado"""
        return 0

    @abc.abstractmethod
    def update(self) -> int:
        """Atualiza uma linha no banco de dados, retorna a quantidade de linhas atualizadas"""
        return 0

    @abc.abstractmethod
    def delete(self) -> int:
        """Remove uma linha no banco de dados, retorna a quantidade de linhas removidas"""
        return 0

    @abc.abstractmethod
    def select(self, identifier):
        """Busca uma linha pelo id"""
        return

    @abc.abstractmethod
    def all(self):
        """Busca todas as linhas do tabela"""
        return

    @staticmethod
    @abc.abstractmethod
    def create_table():
        """Cria tabela no banco de dados"""
        return

    @staticmethod
    @abc.abstractmethod
    def insert_dummy():
        """Insere valores padrão no banco de dados"""
        return

    @staticmethod
    @abc.abstractmethod
    def has_ownership() -> bool:
        """Identifica entidades que estão relacionadas a algum usuário"""
        return False

    @abc.abstractmethod
    def get_owner_id(self) -> int:
        """Retorna o id do usuário relacionado"""
        return 0

    @abc.abstractmethod
    def get_owner(self):
        """Retorna o usuário relacionado"""
        return None
