from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

@event.listens_for(Engine, "checkout")
def set_db_role_on_checkout(dbapi_connection, connection_record, connection_proxy):
    from flask import g, has_app_context
    try:
        cursor = dbapi_connection.cursor()
        # Solo intentamos usar g si estamos en un contexto de aplicación
        if has_app_context() and hasattr(g, 'db_role') and g.db_role:
            cursor.execute(f"SET ROLE '{g.db_role}'")
        else:
            # Por defecto, usamos el rol base (cliente_rol) o el DEFAULT configurado en BD
            cursor.execute("SET ROLE DEFAULT")
        cursor.close()
    except Exception as e:
        print(f"DEBUG: Error setting DB role: {e}")
