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
    def insert(self):
        """Método para inserir de uma linha no banco de dados"""
        return

    @abc.abstractmethod
    def update(self):
        """Método para atualizar uma linha no banco de dados"""
        return

    @abc.abstractmethod
    def delete(self):
        """Método para remover uma linha no banco de dados"""
        return

    @abc.abstractmethod
    def select(self, identifier):
        """Método para busca uma linha pelo id"""
        return

    @abc.abstractmethod
    def all(self):
        """Método para busca todas as linhas do tabela"""
        return
