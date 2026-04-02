from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

# == Manejo de Sesiones mediante Roles de BD ==
# NOTA PARA DESARROLLO: Se mantiene comentado temporalmente para evitar problemas de permisos de BD local.
# Se debe activar solo en entorno de Producción si los roles PostgreSQL/MySQL están configurados.
#
# @event.listens_for(Engine, "checkout")
# def set_db_role_on_checkout(dbapi_connection, connection_record, connection_proxy):
#     from flask import g
#     try:
#         cursor = dbapi_connection.cursor()
#         # Asumiendo que guardamos el rol del usuario en `g.db_role` al inicio de cada petición
#         if hasattr(g, 'db_role') and g.db_role:
#             cursor.execute(f"SET ROLE {g.db_role}")
#         else:
#             cursor.execute("RESET ROLE") # Retorna al rol administrador/default del pool
#         cursor.close()
#     except Exception as e:
#         pass

