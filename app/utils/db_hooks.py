import os
from sqlalchemy import text
from app.utils.database_connection import db

def init_db_objects(app):
    """Inicializa procedimientos almacenados y roles de base de datos."""
    sql_dir = os.path.join(app.root_path, 'database')
    
    sql_files = [
        'sp_procesar_venta_hibrida.sql'
    ]
    
    with app.app_context():
        for filename in sql_files:
            file_path = os.path.join(sql_dir, filename)
            if not os.path.exists(file_path):
                print(f"Advertencia: No se encontró el archivo {file_path}")
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                if filename.endswith('.sql'):
                    statements = []
  
                    if 'DELIMITER //' in sql_content:
                        sql_clean = sql_content.replace('DELIMITER //', '').replace('DELIMITER ;', '').replace('//', ';')
                        import re
                        match = re.search(r'CREATE\s+PROCEDURE\s+([^\(\s]+)', sql_clean, re.IGNORECASE)
                        if match:
                            sp_name = match.group(1)
                            db.session.execute(text(f"DROP PROCEDURE IF EXISTS {sp_name}"))
                        db.session.execute(text(sql_clean))
                    else:
                        # Scripts normales (como el de roles)
                        for stmt in sql_content.split(';'):
                            stmt = stmt.strip()
                            if stmt:
                                db.session.execute(text(stmt))
                                
                db.session.commit()
                print(f"Objeto de BD '{filename}' cargado/actualizado correctamente.")
            except Exception as e:
                db.session.rollback()
                print(f"Error al cargar {filename}: {str(e)}")
