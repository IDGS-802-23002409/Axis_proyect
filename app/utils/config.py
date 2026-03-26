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

# # Configuración básica de seguridad
#app.config['SECURITY_REGISTERABLE'] = True
#app.config['SECURITY_CONFIRMABLE'] = True
#app.config['SECURITY_RECOVERABLE'] = True
#app.config['SECURITY_CHANGEABLE'] = True

# # Configuración de 2FA
#app.config['SECURITY_TWO_FACTOR'] = True
#app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['authenticator', 'email']
#app.config['SECURITY_TWO_FACTOR_REQUIRED'] = True
#app.config['SECURITY_TWO_FACTOR_ALWAYS_ASK'] = True

# # Servidor de Correo (Necesario para enviar los códigos y confirmaciones)
#app.config['MAIL_SERVER'] = 'smtp.tuproveedor.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = 'tu-correo@ejemplo.com'
#app.config['MAIL_PASSWORD'] = 'tu-password'