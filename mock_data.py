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
            db.session.add_all([cat1, cat2, cat3])
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
        default_img = "/static/images/default/default-image.png"
        if not ModeloRopa.query.first():
            m1 = ModeloRopa(nombre_modelo="Camiseta Oversize Core", descripcion="Camiseta holgada de algodón urbano.", uuid_categoria=categorias[0].uuid_categoria, imagen_url=default_img)
            m2 = ModeloRopa(nombre_modelo="Cargo Pants Black", descripcion="Pantalones cargo oscuros con multibolso.", uuid_categoria=categorias[1].uuid_categoria, imagen_url=default_img)
            m3 = ModeloRopa(nombre_modelo="Hoodie Essential", descripcion="Sudadera clásica con gorro.", uuid_categoria=categorias[2].uuid_categoria, imagen_url=default_img)
            
            db.session.add_all([m1, m2, m3])
            db.session.commit()
            
            # Asociar tallas a m1
            for talla in ['S', 'M', 'L']:
                db.session.add(ProductoTerminado(sku_especifico=f"CORE-OVR-{talla}", uuid_modelo=m1.uuid_modelo, talla=talla, precio_venta=400.00))
            
            # Asociar tallas a m2
            for talla in ['M', 'L', 'XL']:
                db.session.add(ProductoTerminado(sku_especifico=f"CRG-BLK-{talla}", uuid_modelo=m2.uuid_modelo, talla=talla, precio_venta=850.00))

            db.session.commit()
            print(" [OK] Modelos padre y sub-tallas (SKUs) creadas exitosamente.")
            
        print("\n>> ¡Inyección de datos Mock completada con éxito! 🎉")
        print("   Email Test Admin: admin@axis.com / Pass: admin1234")

if __name__ == '__main__':
    run_seed()
