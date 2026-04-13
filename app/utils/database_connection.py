from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

# @event.listens_for(Engine, "checkout")
# def set_db_role_on_checkout(dbapi_connection, connection_record, connection_proxy):
#     from flask import g
#     try:
#         cursor = dbapi_connection.cursor()
#         if hasattr(g, 'db_role') and g.db_role:
#             cursor.execute(f"SET ROLE '{g.db_role}'")
#         else:
#             # En lugar de NONE, volvemos a DEFAULT para permitir que scripts de sistema (como create_all) 
#             # usen los permisos base del usuario/admin.
#             cursor.execute("SET ROLE DEFAULT")
#         cursor.close()
#     except Exception:
#         pass
