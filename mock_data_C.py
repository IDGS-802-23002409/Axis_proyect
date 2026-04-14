import sys
import os
import uuid
from datetime import datetime, timezone, timedelta

# Asegurar que importamos desde el root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

# Importar modelos necesarios para usuarios
from app.models.usuarios import Usuario, Role
from app.models.empleados import Empleado
from app.models.clientes import Cliente

def run_seed():
    with app.app_context():
        print(">> [INICIO] Creando datos de prueba (Solo Usuarios)...")

        # 1. ROLES DE SEGURIDAD
        roles_names = ['admin', 'gerente', 'produccion', 'cliente']
        roles_dict = {}
        for r_name in roles_names:
            role = Role.query.filter_by(name=r_name).first()
            if not role:
                role = Role(name=r_name)
                db.session.add(role)
            roles_dict[r_name] = role
        db.session.commit()
        print(" [OK] Roles creados.")

        # 2. USUARIOS Y PERFILES
        test_users = [
            {
                "nombre": "Admin Axis",
                "email": "admin@axis.com",
                "pass": "admin1234",
                "role": "admin",
                "emp_num": "EMP-001",
                "puesto": "Director General",
                "depto": "Dirección"
            },
            {
                "nombre": "Modista Principal",
                "email": "modista@axis.com",
                "pass": "modista1234",
                "role": "produccion",
                "emp_num": "EMP-002",
                "puesto": "Jefe de Taller",
                "depto": "Producción"
            },
            {
                "nombre": "Vendedor Axis",
                "email": "ventas@axis.com",
                "pass": "ventas1234",
                "role": "gerente",
                "emp_num": "EMP-003",
                "puesto": "Ejecutivo Comercial",
                "depto": "Ventas"
            },
            {
                "nombre": "Comprador Axis",
                "email": "compras@axis.com",
                "pass": "compras1234",
                "role": "produccion",
                "emp_num": "EMP-004",
                "puesto": "Analista de Suministros",
                "depto": "Compras"
            },
            {
                "nombre": "Juan Cliente",
                "email": "juan@axis.com",
                "pass": "cliente1234",
                "role": "cliente",
                "tel": "555-123-4567",
                "dir": "Av. Reforma 123, CDMX"
            },
            {
                "nombre": "Maria Lopez",
                "email": "maria@axis.com",
                "pass": "cliente1234",
                "role": "cliente",
                "tel": "555-987-6543",
                "dir": "Insurgentes Sur 456, CDMX"
            }
        ]

        for u in test_users:
            user = Usuario.query.filter_by(email=u["email"]).first()
            if not user:
                now = datetime.now(timezone.utc)
                user = Usuario(
                    nombre_completo=u["nombre"],
                    email=u["email"],
                    password=hash_password(u["pass"]),
                    active=True,
                    fs_uniquifier=uuid.uuid4().hex,
                    confirmed_at=now,
                    password_changed_at=now,
                )
                user.roles.append(roles_dict[u["role"]])
                db.session.add(user)
                db.session.flush()

                # Crear perfil de empleado o cliente según el rol
                if u["role"] in ['admin', 'produccion', 'gerente']:
                    if not Empleado.query.filter_by(uuid_usuario=user.uuid_usuario).first():
                        db.session.add(Empleado(
                            uuid_usuario=user.uuid_usuario,
                            numero_empleado=u["emp_num"],
                            puesto=u["puesto"],
                            departamento=u["depto"],
                            fecha_ingreso=datetime.now(timezone.utc) - timedelta(days=365)
                        ))
                elif u["role"] == 'cliente':
                    if not Cliente.query.filter_by(uuid_usuario=user.uuid_usuario).first():
                        db.session.add(Cliente(
                            uuid_usuario=user.uuid_usuario,
                            telefono=u["tel"],
                            direccion_completa=u["dir"]
                        ))
                print(f" [OK] Usuario '{u['email']}' creado.")
        
        db.session.commit()
        print("\n>> [ÉXITO] Datos de prueba completados. Solo usuarios y perfiles.")


if __name__ == '__main__':
    run_seed()
