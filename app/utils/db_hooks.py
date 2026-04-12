import os
from sqlalchemy import text
from app.utils.database_connection import db

def init_stored_procedures(app):
    sql_dir = os.path.join(app.root_path, 'database')
    
    sp_files = ['sp_procesar_venta_hibrida.sql']
    
    with app.app_context():
        for filename in sp_files:
            file_path = os.path.join(sql_dir, filename)
            if not os.path.exists(file_path):
                print(f"Error: No se encontró el archivo {file_path}")
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                sql_clean = sql_content.replace('DELIMITER //', '').replace('DELIMITER ;', '').replace('//', '')
                import re
                match = re.search(r'CREATE\s+PROCEDURE\s+([^\(\s]+)', sql_clean, re.IGNORECASE)
                if match:
                    sp_name = match.group(1)
                    db.session.execute(text(f"DROP PROCEDURE IF EXISTS {sp_name}"))
                
                db.session.execute(text(sql_clean))
                db.session.commit()
                print(f"Stored Procedure '{filename}' cargado/actualizado correctamente.")
            except Exception as e:
                db.session.rollback()
                print(f"Error al cargar SP {filename}: {str(e)}")
