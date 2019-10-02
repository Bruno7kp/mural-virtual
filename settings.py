from dotenv import load_dotenv
from pathlib import Path
import os

# Carrega arquivo .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configurações do banco de dados
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
