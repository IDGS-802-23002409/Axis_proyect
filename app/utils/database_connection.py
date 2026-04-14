from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app.utils.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    ADMIN_DB_USER, ADMIN_DB_PASSWORD,
    GERENTE_DB_USER, GERENTE_DB_PASSWORD,
    PRODUCCION_DB_USER, PRODUCCION_DB_PASSWORD,
    CLIENTE_DB_USER, CLIENTE_DB_PASSWORD,
    BACKUP_DB_USER, BACKUP_DB_PASSWORD
)

db = SQLAlchemy()

# Diccionario para cachear los engines de cada rol
_engines = {}

def get_engine_for_role(role_name):
    """
    Retorna un engine de SQLAlchemy configurado con las credenciales 
    específicas para el rol solicitado.
    """
    if role_name in _engines:
        return _engines[role_name]
    
    # Mapeo de roles de sistema a credenciales de BD
    creds = {
        'admin_rol': (ADMIN_DB_USER, ADMIN_DB_PASSWORD),
        'gerente_rol': (GERENTE_DB_USER, GERENTE_DB_PASSWORD),
        'produccion_rol': (PRODUCCION_DB_USER, PRODUCCION_DB_PASSWORD),
        'cliente_rol': (CLIENTE_DB_USER, CLIENTE_DB_PASSWORD),
        'backup_rol': (BACKUP_DB_USER, BACKUP_DB_PASSWORD),
        'default': (DB_USER, DB_PASSWORD)
    }
    
    user, password = creds.get(role_name, creds['default'])
    
    uri = f"mysql+pymysql://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(uri, pool_pre_ping=True, pool_recycle=3600)
    _engines[role_name] = engine
    return engine
