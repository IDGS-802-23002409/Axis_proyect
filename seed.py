import os
import uuid
from faker import Faker
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.models.usuarios import Usuario, Role
from app.models.clientes import Cliente
from app.models.categorias import Categoria
from app.models.insumos import Insumo
from app.models.proveedores import Proveedor
from app.models.modelos_productos import ModeloRopa, ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera, ExplosionMaterialesDetalle
from app.models.compras import CompraEncabezado, CompraDetalle
from app.models.inventario import RolloInventario, RetazoInventario
from app.models.produccion import OrdenProduccion, EjecucionCorte
from app.models.ventas import VentaEncabezado, VentaDetalle

# Configurar Faker
fake = Faker('es_MX')  # Español mexicano para datos locales

# Configurar DB
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    print("Iniciando seeding de datos...")

    # 1. Roles
    print("Creando roles...")
    roles = [
        Role(name='admin', description='Administrador del sistema'),
        Role(name='cliente', description='Usuario cliente'),
        Role(name='produccion', description='Usuario de producción'),
        Role(name='gerente', description='Usuario de gerencia'),
    ]
    session.add_all(roles)
    session.commit()

    # 2. Usuarios
    print("Creando usuarios...")
    usuarios = []
    for i in range(15):  # 15 usuarios
        email = fake.email()
        password_hash = generate_password_hash('password123')
        fs_uniquifier = uuid.uuid4().hex
        usuario = Usuario(
            nombre_completo=fake.name(),
            email=email,
            password=password_hash,
            active=True,
            fs_uniquifier=fs_uniquifier,
            confirmed_at=fake.date_time_this_year(),
            tf_primary_method='email' if i % 2 == 0 else None,
            tf_totp_secret=fake.sha256() if i % 2 == 0 else None,
        )
        if i < 3:
            usuario.roles.append(roles[0])  # Admin
        elif i < 10:
            usuario.roles.append(roles[1])  # Cliente
        else:
            usuario.roles.append(roles[2])  # Produccion
        usuarios.append(usuario)
    session.add_all(usuarios)
    session.commit()

    # 3. Clientes (asociados a usuarios clientes)
    print("Creando clientes...")
    clientes = []
    cliente_usuarios = [u for u in usuarios if 'cliente' in [r.name for r in u.roles]]
    for i, user in enumerate(cliente_usuarios):
        cliente = Cliente(
            uuid_usuario=user.uuid_usuario,
            telefono=fake.phone_number(),
            direccion_completa=fake.address(),
        )
        clientes.append(cliente)
    session.add_all(clientes)
    session.commit()

    # 4. Categorias
    print("Creando categorías...")
    categorias = [
        Categoria(nombre='Camisetas', descripcion='Ropa superior casual', estatus_visible=True),
        Categoria(nombre='Pantalones', descripcion='Ropa inferior', estatus_visible=True),
        Categoria(nombre='Vestidos', descripcion='Ropa formal para mujeres', estatus_visible=True),
        Categoria(nombre='Chaquetas', descripcion='Ropa exterior', estatus_visible=True),
        Categoria(nombre='Faldas', descripcion='Ropa inferior para mujeres', estatus_visible=True),
        Categoria(nombre='Shorts', descripcion='Ropa corta de verano', estatus_visible=True),
        Categoria(nombre='Blusas', descripcion='Ropa superior elegante', estatus_visible=True),
        Categoria(nombre='Sudaderas', descripcion='Ropa deportiva', estatus_visible=True),
        Categoria(nombre='Jeans', descripcion='Pantalones de mezclilla', estatus_visible=True),
        Categoria(nombre='Accesorios', descripcion='Complementos de ropa', estatus_visible=True),
    ]
    session.add_all(categorias)
    session.commit()

    # 5. Proveedores
    print("Creando proveedores...")
    proveedores = []
    for i in range(10):
        proveedor = Proveedor(
            razon_social=fake.company(),
            rfc=fake.ssn(),
            contacto_nombre=fake.name(),
        )
        proveedores.append(proveedor)
    session.add_all(proveedores)
    session.commit()

    # 6. Insumos
    print("Creando insumos...")
    insumos = []
    tipos_insumo = ['Tela de algodón', 'Hilo', 'Botones', 'Cierres', 'Tela sintética', 'Tejido elástico', 'Cuero', 'Lana', 'Seda', 'Lino']
    for i in range(15):
        insumo = Insumo(
            sku=f'SKU{i+1:03d}',
            nombre=tipos_insumo[i % len(tipos_insumo)] + f' {i+1}',
            uuid_categoria=categorias[i % len(categorias)].uuid_categoria,
            costo_unitario_individual=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            stock_minimo_alerta=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
        )
        insumos.append(insumo)
    session.add_all(insumos)
    session.commit()

    # 7. Modelos de Ropa
    print("Creando modelos de ropa...")
    modelos = []
    for i in range(12):
        modelo = ModeloRopa(
            nombre_modelo=f'Modelo {fake.word().capitalize()} {i+1}',
            descripcion=fake.sentence(),
            uuid_categoria=categorias[i % len(categorias)].uuid_categoria,
        )
        modelos.append(modelo)
    session.add_all(modelos)
    session.commit()

    # 8. Productos Terminados
    print("Creando productos terminados...")
    productos = []
    tallas = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    for modelo in modelos:
        for talla in tallas:
            producto = ProductoTerminado(
                uuid_modelo=modelo.uuid_modelo,
                sku_especifico=f'{modelo.nombre_modelo.replace(" ", "")}-{talla}',
                talla=talla,
                precio_venta=fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=50),
                stock_minimo_alerta=fake.random_int(min=5, max=20),
            )
            productos.append(producto)
    session.add_all(productos)
    session.commit()

    # 9. Explosion de Materiales
    print("Creando explosión de materiales...")
    for producto in productos[:10]:  # Solo para algunos productos
        cabecera = ExplosionMaterialesCabecera(
            uuid_producto=producto.uuid_producto,
            instrucciones_proceso=fake.text(max_nb_chars=200),
        )
        session.add(cabecera)
        session.commit()  # Para obtener uuid_explosion

        # Detalles
        for j in range(fake.random_int(min=2, max=5)):
            detalle = ExplosionMaterialesDetalle(
                uuid_explosion=cabecera.uuid_explosion,
                uuid_insumo=fake.random_element(insumos).uuid_insumo,
                consumo_teorico_unitario=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                ancho_referencia=fake.pydecimal(left_digits=2, right_digits=1, positive=True),
            )
            session.add(detalle)
    session.commit()

    # 10. Compras
    print("Creando compras...")
    for i in range(10):
        encabezado = CompraEncabezado(
            folio_factura=f'FAC{i+1:04d}',
            uuid_proveedor=fake.random_element(proveedores).uuid_proveedor,
            uuid_usuario_registro=fake.random_element(usuarios).uuid_usuario,
            estatus=fake.random_element(['Pendiente', 'Recibido']),
        )
        session.add(encabezado)
        session.commit()

        # Detalles
        for j in range(fake.random_int(min=1, max=3)):
            detalle = CompraDetalle(
                uuid_compra=encabezado.uuid_compra,
                uuid_insumo=fake.random_element(insumos).uuid_insumo,
                cantidad_comprada=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                unidad_medida='metros',
                costo_unitario_compra=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
            )
            session.add(detalle)
    session.commit()

    # 11. Inventario (Rollos)
    print("Creando inventario...")
    rollos = []
    for compra_detalle in session.query(CompraDetalle).all()[:15]:
        rollo = RolloInventario(
            uuid_insumo=compra_detalle.uuid_insumo,
            uuid_detalle_compra=compra_detalle.uuid_detalle_compra,
            metraje_inicial=compra_detalle.cantidad_comprada,
            metraje_continuo_actual=compra_detalle.cantidad_comprada,
            ancho_real_recibido=fake.pydecimal(left_digits=2, right_digits=1, positive=True),
        )
        rollos.append(rollo)
    session.add_all(rollos)
    session.commit()

    # 12. Producción (Ordenes)
    print("Creando órdenes de producción...")
    ordenes = []
    for i in range(10):
        orden = OrdenProduccion(
            uuid_producto=fake.random_element(productos).uuid_producto,
            cantidad_a_producir=fake.random_int(min=10, max=100),
            estado=fake.random_element(['Pendiente', 'En Corte', 'Confección', 'Terminado']),
        )
        ordenes.append(orden)
    session.add_all(ordenes)
    session.commit()

    # 13. Ejecución de Corte
    print("Creando ejecuciones de corte...")
    for orden in ordenes[:8]:
        ejecucion = EjecucionCorte(
            uuid_op=orden.uuid_op,
            uuid_rollo_usado=fake.random_element(rollos).uuid_rollo,
            metros_sacados_bodega=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
            prendas_reales_logradas=fake.random_int(min=5, max=50),
            merma_real_calculada=fake.pydecimal(left_digits=1, right_digits=2, positive=True),
        )
        session.add(ejecucion)
    session.commit()

    # 14. Ventas
    print("Creando ventas...")
    for i in range(10):
        encabezado = VentaEncabezado(
            numero_pedido=f'PED{i+1:04d}',
            uuid_cliente=fake.random_element(clientes).uuid_cliente,
            metodo_pago=fake.random_element(['Tarjeta', 'Efectivo', 'Transferencia']),
            estatus_envio=fake.random_element(['Procesando', 'Enviado', 'Entregado']),
        )
        session.add(encabezado)
        session.commit()

        # Detalles
        for j in range(fake.random_int(min=1, max=3)):
            detalle = VentaDetalle(
                uuid_venta=encabezado.uuid_venta,
                uuid_producto=fake.random_element(productos).uuid_producto,
                cantidad=fake.random_int(min=1, max=5),
                precio_unitario_historico=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            )
            session.add(detalle)
    session.commit()

    print("Seeding completado exitosamente!")

if __name__ == '__main__':
    seed_data()