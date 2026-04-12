import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

from app.models.usuarios import Usuario, Role
from app.models.empleados import Empleado
from app.models.clientes import Cliente
from app.models.insumos import Insumo
from app.models.categorias import Categoria


def run_seed():
    with app.app_context():
        print(">> [INICIO] Creando datos de prueba...")

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

        db.session.commit()
        print(" [OK] Usuarios creados.")

                # ─────────────────────────────
        # 3. CATEGORÍAS
        # ─────────────────────────────
        categorias_data = [
            # ── Categorías de Insumos ──
            {"nombre": "Telas",             "descripcion": "Tipos de telas",          "tipo": "Insumo"},
            {"nombre": "Cinta tapacostura", "descripcion": "Cintas",                  "tipo": "Insumo"},
            {"nombre": "Hilo",              "descripcion": "Hilos",                   "tipo": "Insumo"},
            {"nombre": "Rib de algodon",    "descripcion": "Rib",                     "tipo": "Insumo"},
            {"nombre": "Etiquetas",         "descripcion": "Etiquetas",               "tipo": "Insumo"},
            {"nombre": "Estampados",        "descripcion": "Estampados",              "tipo": "Insumo"},
            {"nombre": "Ojalillos",         "descripcion": "Ojales",                  "tipo": "Insumo"},
            {"nombre": "Forro",             "descripcion": "Forro",                   "tipo": "Insumo"},
            {"nombre": "Cierre",            "descripcion": "Cierres",                 "tipo": "Insumo"},
            {"nombre": "Botones",           "descripcion": "Botones",                 "tipo": "Insumo"},
            {"nombre": "Remaches",          "descripcion": "Remaches",                "tipo": "Insumo"},
            {"nombre": "Elastico",          "descripcion": "Elásticos",               "tipo": "Insumo"},

            # ── Categorías de Prendas ──
            {"nombre": "Playeras",          "descripcion": "Playeras y camisetas",    "tipo": "Prenda"},
            {"nombre": "Pantalones",        "descripcion": "Pantalones y jeans",      "tipo": "Prenda"},
            {"nombre": "Vestidos",          "descripcion": "Vestidos y faldas",       "tipo": "Prenda"},
            {"nombre": "Sudaderas",         "descripcion": "Sudaderas y hoodies",     "tipo": "Prenda"},
            {"nombre": "Chamarras",         "descripcion": "Chamarras y abrigos",     "tipo": "Prenda"},
            {"nombre": "Shorts",            "descripcion": "Shorts y bermudas",       "tipo": "Prenda"},
        ]

        categorias_dict = {}

        for c in categorias_data:
            categoria = Categoria.query.filter_by(nombre=c["nombre"], tipo=c["tipo"]).first()
            if not categoria:
                categoria = Categoria(
                    nombre=c["nombre"],
                    descripcion=c["descripcion"],
                    tipo=c["tipo"]
                )
                db.session.add(categoria)
                db.session.flush()

            categorias_dict[c["nombre"]] = categoria

        db.session.commit()
        print(" [OK] Categorías creadas.")

        # ─────────────────────────────
        # 4. INSUMOS
        # ─────────────────────────────
        insumos_data = [

            # ───── TELAS (ROLLOS) ─────
            {
                "sku": "TEL-JER-NEG-001",
                "nombre": "Tela Jersey Algodón Negra",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 100,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 50,
                "ancho": 2.0
            },
            {
                "sku": "TEL-FEL-NEG-001",
                "nombre": "Tela Felpa Negra",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 40,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 30,
                "ancho": 2.0
            },
            {
                "sku": "TEL-GAB-001",
                "nombre": "Gabardina Poliéster",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.50
            },
            {
                "sku": "TEL-MEZ-AZUL-001",
                "nombre": "Mezclilla Azul",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 40,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.50
            },
            {
                "sku": "TEL-POLALG-NEG-001",
                "nombre": "Tela Poliéster/Algodón Negra",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 30,
                "ancho": 1.75
            },

            # ───── RIB (ROLLOS) ─────
            {
                "sku": "RIB-NEG-001",
                "nombre": "Rib Negro",
                "categoria": "Rib de algodon",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 30,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 0.50
            },
            {
                "sku": "RIB-BEI-001",
                "nombre": "Rib Beige",
                "categoria": "Rib de algodon",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 30,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 15,
                "ancho": 0.60
            },

            # ───── HILO (AHORA ROLLO  CORREGIDO) ─────
            {
                "sku": "HIL-POL-NEG-001",
                "nombre": "Hilo Negro 40/2",
                "categoria": "Hilo",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 3000,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 10
            },
            {
                "sku": "HIL-POL-BEI-001",
                "nombre": "Hilo Beige 40/2",
                "categoria": "Hilo",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 3000,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 10
            },

            # ───── FORRO (ROLLO) ─────
            {
                "sku": "FOR-TAF-001",
                "nombre": "Forro Tafeta",
                "categoria": "Forro",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.40
            },

            # ───── CINTAS (ROLLOS) ─────
            {
                "sku": "CIN-TAPA-NEG-001",
                "nombre": "Cinta Tapacostura Negra",
                "categoria": "Cinta tapacostura",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 100,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 80,
                "ancho": 0.10
            },
            {
                "sku": "CIN-VIVO-BLA-001",
                "nombre": "Cinta Vivo Blanca",
                "categoria": "Cinta tapacostura",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 100,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 0.02
            },

            # ───── ELÁSTICO (ROLLO) ─────
            {
                "sku": "ELA-NEG-004CM-001",
                "nombre": "Elástico Negro 4cm",
                "categoria": "Elastico",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 0.04
            },

            # ───── PIEZAS ─────
            {
                "sku": "CIE-FRON-001",
                "nombre": "Cierre Frontal",
                "categoria": "Cierre",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 20
            },
            {
                "sku": "BTN-GOL-001",
                "nombre": "Botón Metálico",
                "categoria": "Botones",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 50
            },
            {
                "sku": "REM-MET-001",
                "nombre": "Remaches Metálicos",
                "categoria": "Remaches",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "OJA-MET-001",
                "nombre": "Ojalillos Metálicos",
                "categoria": "Ojalillos",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },

            # ───── RESTO IGUAL (PIEZAS) ─────
            {
                "sku": "EST-LOWKEY-001",
                "nombre": "Estampado Lowkey",
                "categoria": "Estampados",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 50
            },
            {
                "sku": "EST-PERS-001",
                "nombre": "Estampado Personalizado",
                "categoria": "Estampados",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 30
            },
        ]


        for i in insumos_data:
            insumo = Insumo.query.filter_by(sku=i["sku"]).first()

            if not insumo:
                db.session.add(
                    Insumo(
                        sku=i["sku"],
                        nombre=i["nombre"],
                        uuid_categoria=categorias_dict[i["categoria"]].uuid_categoria,
                        unidad_medida=i["unidad_medida"],
                        contenido_cantidad=i["contenido_cantidad"],
                        contenido_unidad_medida=i["contenido_unidad_medida"],
                        stock_total_acumulado=i["stock"],
                        stock_minimo_alerta=i["stock_min"],
                        ancho=i.get("ancho"),
                        usuario_actualizo_uuid=None,
                    )
                )

                print(f" [OK] Insumo '{i['nombre']}' creado.")

        db.session.commit()
        print(" [OK] Insumos creados.")

        print("\n>> [ÉXITO] Seed completo.")


if __name__ == '__main__':
    run_seed()