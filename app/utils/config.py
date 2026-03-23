import os
from dotenv import load_dotenv

# Carga variables de entorno desde un archivo .env (si existe)
load_dotenv()

# Leer variables de entorno (puedes usar .env o exportarlas en el sistema)
DB_USER = os.getenv('DB_USER', 'flask_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'flask_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'flask_db')