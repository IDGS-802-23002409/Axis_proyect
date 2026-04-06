import sys
import os

# Asegurar que importamos desde el root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

from app.models.usuarios import Usuario, Role
from app.models.empleados import Empleado
from app.models.clientes import Cliente
from app.models.proveedores import Proveedor
from app.models.categorias import Categoria
from app.models.modelos_productos import ModeloRopa, ProductoTerminado
from app.models.insumos import Insumo
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from datetime import datetime, timezone

def run_seed():
    with app.app_context():
        print(">> Iniciando inyección de datos Mock...")
        
        # 1. Crear Roles de Seguridad si no existen
        roles_names = ['admin', 'gerente', 'produccion', 'cliente']
        roles_dict = {}
        for r_name in roles_names:
            role = Role.query.filter_by(name=r_name).first()
            if not role:
                role = Role(name=r_name)
                db.session.add(role)
            roles_dict[r_name] = role
        db.session.commit()
        print(" [OK] Roles verificados.")

        # 2. Crear Usuarios (Admins, Clientes, Empleados)
        test_users = [
            {"nombre": "Admin Axis", "email": "admin@axis.com", "pass": "admin1234", "role": "admin", "emp_num": "EMP-001", "puesto": "Director Tienda", "depto": "Gerencia"},
            {"nombre": "Empleado Modista", "email": "modista@axis.com", "pass": "modista1234", "role": "produccion", "emp_num": "EMP-002", "puesto": "Sastre Principal", "depto": "Produccion"},
            {"nombre": "Juan Cliente", "email": "juan@axis.com", "pass": "cliente1234", "role": "cliente", "tel": "555-123-4567", "dir": "Av. Siempre Viva 742"}
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
                db.session.flush() # Para tener el uuid

                # Ligar perfil operativo
                if u["role"] in ['admin', 'produccion']:
                    if not Empleado.query.filter_by(uuid_usuario=user.uuid_usuario).first() and \
                       not Empleado.query.filter_by(numero_empleado=u["emp_num"]).first():
                        db.session.add(Empleado(
                            uuid_usuario=user.uuid_usuario, 
                            numero_empleado=u["emp_num"], 
                            puesto=u["puesto"], 
                            departamento=u["depto"]
                        ))
                elif u["role"] == 'cliente':
                    if not Cliente.query.filter_by(uuid_usuario=user.uuid_usuario).first():
                        db.session.add(Cliente(
                            uuid_usuario=user.uuid_usuario, 
                            telefono=u["tel"], 
                            direccion_completa=u["dir"]
                        ))
                print(f" [OK] Usuario {u['email']} creado.")
        
        db.session.commit()

        # Admin for recipes
        admin_user = Usuario.query.filter_by(email="admin@axis.com").first()
        admin_uuid = admin_user.uuid_usuario if admin_user else None

        # 3. Categorías
        if not Categoria.query.first():
            cat1 = Categoria(nombre="Camisetas", descripcion="Prendas de cuerpo superior", estatus_visible=True)
            cat2 = Categoria(nombre="Pantalones", descripcion="Prendas inferiores", estatus_visible=True)
            cat3 = Categoria(nombre="Hoodies", descripcion="Sudaderas con gorro", estatus_visible=True)
            cat4 = Categoria(nombre="Chaquetas", descripcion="Abrigos y chamarras", estatus_visible=True)
            cat5 = Categoria(nombre="Shorts", descripcion="Pantalones cortos", estatus_visible=True)
            cat6 = Categoria(nombre="Accesorios", descripcion="Gorras y complementos", estatus_visible=True)
            db.session.add_all([cat1, cat2, cat3, cat4, cat5, cat6])
            db.session.commit()
            print(" [OK] Categorías creadas.")
        else:
            # Asegurar que las existentes sean visibles
            for c in Categoria.query.all():
                c.estatus_visible = True
            db.session.commit()
            print(" [INFO] Categorías existentes marcadas como visibles.")
            
        categorias = Categoria.query.all()

        # 4. Proveedores e Insumos
        if not Proveedor.query.first():
            prov1 = Proveedor(
                razon_social="Telastika SA", 
                rfc="TELA010101XXX", 
                contacto_nombre="Pedro",
                telefono="555-987-6543",
                categoria_insumo="Textiles"
            )
            db.session.add(prov1)
            db.session.commit()
            
            ins1 = Insumo(sku="INS-001", nombre="Algodón Premium Negro", uuid_categoria=categorias[0].uuid_categoria, unidad_medida="ROLLO", contenido_cantidad=100.0, contenido_unidad_medida="METRO")
            ins2 = Insumo(sku="INS-002", nombre="Botones Metálicos", uuid_categoria=categorias[1].uuid_categoria, unidad_medida="PIEZA", contenido_cantidad=1.0, contenido_unidad_medida="PIEZA")
            db.session.add_all([ins1, ins2])
            db.session.commit()
            print(" [OK] Proveedores e Insumos creados.")

        # 5. Modelos Matrix (Padre) y Variantes Tallas (Productos Terminados)
        if not ModeloRopa.query.first():
            cats = {c.nombre: c.uuid_categoria for c in categorias}
            
            modelos_data = [
                {"nombre": "Gorra Black Axis", "desc": "Gorra urbana ajustable", "cat": "Accesorios", "img": "cap-black.jpg", "precio": 250.00, "sku": "CAP-BLK"},
                {"nombre": "Cargo Pants Black", "desc": "Pantalón cargo multibolsillo", "cat": "Pantalones", "img": "cargo-pants.jpg", "precio": 850.00, "sku": "CRG-BLK"},
                {"nombre": "Hoodie Essential Black", "desc": "Sudadera clásica oscura", "cat": "Hoodies", "img": "hoodie-black.jpg", "precio": 900.00, "sku": "HD-BLK"},
                {"nombre": "Hoodie Purple Neon", "desc": "Sudadera con tonos púrpuras", "cat": "Hoodies", "img": "hoodie-purple.jpg", "precio": 950.00, "sku": "HD-PUR"},
                {"nombre": "Street Jacket Premium", "desc": "Chaqueta resistente al viento", "cat": "Chaquetas", "img": "jacket-street.jpg", "precio": 1200.00, "sku": "JKT-STR"},
                {"nombre": "Shorts Urban Black", "desc": "Shorts de verano ligeros", "cat": "Shorts", "img": "shorts-black.jpg", "precio": 450.00, "sku": "SH-BLK"},
                {"nombre": "T-Shirt Purple Washed", "desc": "Camiseta con lavado morado", "cat": "Camisetas", "img": "tshirt-purple.jpg", "precio": 400.00, "sku": "TS-PUR"},
                {"nombre": "T-Shirt Classic White", "desc": "Camiseta blanca minimalista", "cat": "Camisetas", "img": "tshirt-white.jpg", "precio": 350.00, "sku": "TS-WHT"}
            ]
            
            # Crear una receta genérica para todos los productos (Explosión de Materiales)
            receta = ExplosionMaterialesCabecera.query.first()
            if not receta:
                receta = ExplosionMaterialesCabecera(
                    instrucciones_proceso="Proceso estándar de fabricación urbana.",
                    uuid_usuario=admin_uuid or "dummy-user-id",
                    estatus='ACTIVO'
                )
                db.session.add(receta)
                db.session.commit()

            for md in modelos_data:
                nuevo_mod = ModeloRopa(
                    nombre_modelo=md["nombre"], 
                    descripcion=md["desc"], 
                    uuid_categoria=cats.get(md["cat"]), 
                    imagen_url=f"/static/images/products/{md['img']}",
                    estatus='ACTIVO'
                )
                db.session.add(nuevo_mod)
                db.session.flush() # Obtener su uuid
                
                # Crear variantes de tallas
                tallas = ['S', 'M', 'L'] if md["cat"] not in ["Accesorios"] else ['Unica']
                for j, talla in enumerate(tallas):
                    db.session.add(ProductoTerminado(
                        sku_especifico=f"{md['sku']}-{talla}", 
                        uuid_modelo=nuevo_mod.uuid_modelo, 
                        uuid_explosion=receta.uuid_explosion,
                        talla=talla, 
                        precio_venta=md["precio"]
                    ))
            
            db.session.commit()
            print(" [OK] Catálogo visual y Modelos base inyectados a partir de las imágenes.")
            
        print("\n>> ¡Inyección de datos Mock completada con éxito! 🎉")
        print("   Email Test Admin: admin@axis.com / Pass: admin1234")

if __name__ == '__main__':
    run_seed()
