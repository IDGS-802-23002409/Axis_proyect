import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

from app.models.usuarios import Usuario, Role
from app.models.empleados import Empleado

def run_seed():
    with app.app_context():
        print(">> [INICIO] Creando Roles y Usuarios principales...")

        # ─────────────────────────────
        # 1. ROLES
        # ─────────────────────────────
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

        # ─────────────────────────────
        # 2. USUARIOS
        # ─────────────────────────────
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
                "nombre": "Gerente Ventas",
                "email": "gerente@axis.com",
                "pass": "gerente1234",
                "role": "gerente",
                "emp_num": "EMP-003",
                "puesto": "Gerente de Ventas",
                "depto": "Ventas"
            }
        ]

        for u in test_users:
            user = Usuario.query.filter_by(email=u["email"]).first()
            if not user:
                user = Usuario(
                    nombre_completo=u["nombre"],
                    email=u["email"],
                    password=hash_password(u["pass"]),
                    confirmed_at=datetime.now(timezone.utc),
                    active=True
                )
                user.roles.append(roles_dict[u["role"]])
                db.session.add(user)
                db.session.flush()

                if u["role"] in ['admin', 'produccion', 'gerente']:
                    db.session.add(Empleado(
                        uuid_usuario=user.uuid_usuario,
                        numero_empleado=u["emp_num"],
                        puesto=u["puesto"],
                        departamento=u["depto"],
                        fecha_ingreso=datetime.now(timezone.utc) - timedelta(days=365)
                    ))
                
                print(f" [OK] Usuario CREADO -> Rol: {u['role'].upper()} | Email: {u['email']} | Pass: {u['pass']}")
            else:
                print(f" [SKIP] Usuario ya existe -> Rol: {u['role'].upper()} | Email: {u['email']}")

        db.session.commit()
        print(">> [ÉXITO] Creación de Roles y Usuarios finalizada.\n")

if __name__ == '__main__':
    run_seed()
