import pymysql
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class DataBase:
    def __init__(self):
        self.con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4')


class BaseModel:
    def __init__(self):
        self.db = DataBase()
