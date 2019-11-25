from datetime import datetime
from typing import List

import pymysql
from flask import jsonify, render_template

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

    @abc.abstractmethod
    def serialize(self):
        """Retorna o objeto que pode ser convertido em json"""
        return {}

    @abc.abstractmethod
    def serialize_array(self):
        """Retorna um array com os valores do objeto"""
        return []


def json_response(message: str, data: List[BaseModel], redirect: str = None):
    return jsonify({
        'message': message,
        'data': [e.serialize() for e in data],
        'redirect': redirect
    })


def data_tables_response(draw: int, total: int, filtered: int, data: List[BaseModel]):
    return jsonify({
        'draw': draw,
        'data': [e.serialize_array() for e in data],
        'recordsTotal': total,
        'recordsFiltered': filtered
    })


def admin_403_response():
    return render_template('admin_403.html'), 403


def admin_404_response():
    return render_template('admin_404.html'), 404


def error_404_response():
    return render_template('404.html'), 404


def show_date(text):
    text = text.__str__()
    return datetime.strptime(text, "%Y-%m-%dT%H:%M").strftime("%d/%m/%Y %H:%M")
