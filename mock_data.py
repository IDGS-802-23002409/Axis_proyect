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
        if not Usuario.query.filter_by(email="admin@axis.com").first():
            admin_user = Usuario(nombre_completo="Admin Axis", email="admin@axis.com", password=hash_password("admin1234"), confirmed_at=datetime.now(timezone.utc), active=True)
            admin_user.roles.append(roles_dict['admin'])
            db.session.add(admin_user)
            
            p_user = Usuario(nombre_completo="Empleado Modista", email="modista@axis.com", password=hash_password("modista1234"), confirmed_at=datetime.now(timezone.utc), active=True)
            p_user.roles.append(roles_dict['produccion'])
            db.session.add(p_user)
            
            c_user = Usuario(nombre_completo="Juan Cliente", email="juan@axis.com", password=hash_password("cliente1234"), confirmed_at=datetime.now(timezone.utc), active=True)
            c_user.roles.append(roles_dict['cliente'])
            db.session.add(c_user)
            
            db.session.commit()

            # Ligar perfiles operativos
            db.session.add(Empleado(uuid_usuario=admin_user.uuid_usuario, numero_empleado="EMP-001", puesto="Director Tienda", departamento="Gerencia"))
            db.session.add(Empleado(uuid_usuario=p_user.uuid_usuario, numero_empleado="EMP-002", puesto="Sastre Principal", departamento="Produccion"))
            db.session.add(Cliente(uuid_usuario=c_user.uuid_usuario, telefono="555-123-4567", direccion_completa="Av. Siempre Viva 742"))
            db.session.commit()
            print(" [OK] Usuarios y Perfiles (Empleados/Clientes) creados.")
        else:
            print(" [INFO] Usuarios ya existían. Saltando...")

        # 3. Categorías
        if not Categoria.query.first():
            cat1 = Categoria(nombre="Camisetas", descripcion="Prendas de cuerpo superior")
            cat2 = Categoria(nombre="Pantalones", descripcion="Prendas inferiores")
            cat3 = Categoria(nombre="Hoodies", descripcion="Sudaderas con gorro")
            cat4 = Categoria(nombre="Chaquetas", descripcion="Abrigos y chamarras")
            cat5 = Categoria(nombre="Shorts", descripcion="Pantalones cortos")
            cat6 = Categoria(nombre="Accesorios", descripcion="Gorras y complementos")
            db.session.add_all([cat1, cat2, cat3, cat4, cat5, cat6])
            db.session.commit()
            print(" [OK] Categorías creadas.")
            
        categorias = Categoria.query.all()

        # 4. Proveedores e Insumos
        if not Proveedor.query.first():
            prov1 = Proveedor(razon_social="Telastika SA", rfc="TELA010101XXX", contacto_nombre="Pedro")
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
            
            for md in modelos_data:
                nuevo_mod = ModeloRopa(
                    nombre_modelo=md["nombre"], 
                    descripcion=md["desc"], 
                    uuid_categoria=cats.get(md["cat"]), 
                    imagen_url=f"/static/images/products/{md['img']}"
                )
                db.session.add(nuevo_mod)
                db.session.flush() # Obtener su uuid
                
                # Crear variantes de tallas
                tallas = ['S', 'M', 'L'] if md["cat"] not in ["Accesorios"] else ['Unica']
                for j, talla in enumerate(tallas):
                    db.session.add(ProductoTerminado(
                        sku_especifico=f"{md['sku']}-{talla}", 
                        uuid_modelo=nuevo_mod.uuid_modelo, 
                        talla=talla, 
                        precio_venta=md["precio"]
                    ))
            
            db.session.commit()
            print(" [OK] Catálogo visual y Modelos base inyectados a partir de las imágenes.")
            
        print("\n>> ¡Inyección de datos Mock completada con éxito! 🎉")
        print("   Email Test Admin: admin@axis.com / Pass: admin1234")

if __name__ == '__main__':
    run_seed()
