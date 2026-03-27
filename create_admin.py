import os
import sys

# Añadir el directorio actual al path para que reconozca el paquete 'app'
sys.path.append(os.getcwd())

from app.app import create_app
from app.utils.database_connection import db
from app.models.usuarios import Role
from flask_security.utils import hash_password

application = create_app()

def create_admin(email, password, name):
    with application.app_context():
        # Obtener el datastore
        ds = application.extensions['security'].datastore
        
        # Crear roles si no existen
        if not Role.query.first():
            print("Inicializando roles básicos...")
            roles = ['admin', 'gerente', 'produccion', 'cliente']
            for r in roles:
                ds.create_role(name=r)
            db.session.commit()

        # Obtener el rol admin
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
             # Fallback: intentar crearlo si falló arriba
            admin_role = ds.create_role(name='admin')
            db.session.commit()

        # Verificar si el usuario ya existe
        if ds.find_user(email=email):
            print(f"Error: El usuario {email} ya existe.")
            return

        # Crear el usuario
        ds.create_user(
            nombre_completo=name,
            email=email,
            password=hash_password(password),
            roles=[admin_role],
            active=True
        )
        db.session.commit()
        print(f"¡Éxito! Usuario administrador creado:")
        print(f"Email: {email}")
        print(f"Password: {password}")

if __name__ == "__main__":
    # Datos por defecto — cámbialos si lo deseas
    create_admin("admin@axis.com", "password123", "Administrador Axis")
