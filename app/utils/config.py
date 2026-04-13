import os
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

# ── Base de Datos ─────────────────────────────
DB_USER = os.getenv('DB_USER', 'flask_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'flask_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'flask_db')

# ── Credenciales de Respaldo ──────────────────
BACKUP_USER = os.getenv('BACKUP_USER', 'backup_user')
BACKUP_PASSWORD = os.getenv('BACKUP_PASSWORD', 'backup_password')

# ── Base de Datos Staging (Incremental Backup) ─
STAGING_DB_USER = os.getenv('STAGING_DB_USER', DB_USER)
STAGING_DB_PASSWORD = os.getenv('STAGING_DB_PASSWORD', DB_PASSWORD)
STAGING_DB_HOST = os.getenv('STAGING_DB_HOST', DB_HOST)
STAGING_DB_PORT = os.getenv('STAGING_DB_PORT', DB_PORT)
STAGING_DB_NAME = os.getenv('STAGING_DB_NAME', 'flask_db_staging')

SECRET_KEY = os.getenv('clave_secreta_axis')

# ── Mail ─────────────────────────────────────
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1')
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

# ── Seguridad ────────────────────────────────
SECURITY_TOTP_SECRETS = os.getenv('SECURITY_TOTP_SECRETS', 'change-me-totp-secret')