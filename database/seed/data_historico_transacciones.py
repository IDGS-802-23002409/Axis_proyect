import sys
import os
import random
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

from app.models.clientes import Cliente
from app.models.usuarios import Usuario, Role
from app.models.compras import CompraEncabezado, CompraDetalle
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.proveedores import Proveedor
from app.models.insumos import Insumo
from app.models.modelos_productos import ProductoTerminado

def generar_clientes():
    print(">> Generando clientes...")
    role_cliente = Role.query.filter_by(name='cliente').first()
    
    if not role_cliente:
        role_cliente = Role(name='cliente')
        db.session.add(role_cliente)
        db.session.commit()

    clientes_data = []
    nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofia", "Jorge", "Lucia"]
    apellidos = ["Perez", "Gomez", "Lopez", "Martinez", "Gonzalez", "Rodriguez", "Hernandez", "Diaz"]

    for i in range(1, 31):
        nombre = f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"
        email = f"cliente{i}@axis.com"
        
        user = Usuario.query.filter_by(email=email).first()
        if not user:
            user = Usuario(
                nombre_completo=nombre,
                email=email,
                password=hash_password("cliente1234"),
                confirmed_at=datetime.now(timezone.utc),
                active=True
            )
            user.roles.append(role_cliente)
            db.session.add(user)
            db.session.flush()

            cliente = Cliente(
                uuid_usuario=user.uuid_usuario,
                telefono=f"477{random.randint(1000000, 9999999)}",
                direccion_completa=f"Calle Falsa {random.randint(100, 999)}, Colonia Centro, Leon Gto"
            )
            db.session.add(cliente)
    
    db.session.commit()
    print(f" [OK] 30 Clientes generados.")

def run_seed():
    with app.app_context():
        print(">> [INICIO] Generando Histórico de Transacciones (Últimos 60 días)...")

        # 1. Generar 30 Clientes Ficticios
        generar_clientes()

        dias_historia = 60
        fecha_actual = datetime.now()

        proveedores = Proveedor.query.all()
        insumos = Insumo.query.all()
        clientes = Cliente.query.all()
        productos = ProductoTerminado.query.all()
        usuario_admin = Usuario.query.filter_by(email="admin@axis.com").first()

        if not (proveedores and insumos and clientes and productos and usuario_admin):
            print("❌ Faltan datos base (proveedores, insumos, clientes, productos, o admin) para generar el histórico.")
            return

        # Dar un stock inicial masivo para que no fallen los constraints si se resta en DB
        for i in insumos:
            i.stock_total_acumulado = float(i.stock_total_acumulado or 0) + 5000.0
        
        for p in productos:
            p.stock_fisico_actual = int(p.stock_fisico_actual or 0) + 5000

        db.session.commit()

        total_compras = 0
        total_ventas = 0

        for dia_offset in range(dias_historia, -1, -1):
            fecha_dia = fecha_actual - timedelta(days=dia_offset)

            # Generar de 1 a 3 compras por día
            num_compras = random.randint(1, 3)
            for _ in range(num_compras):
                fecha_compra = fecha_dia.replace(hour=random.randint(8, 17), minute=random.randint(0, 59))
                proveedor = random.choice(proveedores)

                compra = CompraEncabezado(
                    folio_factura=f"FACT-{fecha_compra.strftime('%Y%m%d')}-{random.randint(100, 999)}",
                    uuid_proveedor=proveedor.uuid_proveedor,
                    uuid_usuario_registro=usuario_admin.uuid_usuario,
                    fecha_compra=fecha_compra,
                    estatus='RECIBIDO'
                )
                db.session.add(compra)
                db.session.flush()

                num_detalles = random.randint(2, 5)
                insumos_compra = random.sample(insumos, k=min(num_detalles, len(insumos)))

                for insumo in insumos_compra:
                    cantidad = random.randint(10, 50)
                    costo_unitario = random.uniform(15.0, 300.0)
                    detalle = CompraDetalle(
                        uuid_compra=compra.uuid_compra,
                        uuid_insumo=insumo.uuid_insumo,
                        cantidad_comprada=cantidad,
                        costo_unitario_compra=costo_unitario,
                        fecha_creacion=fecha_compra
                    )
                    db.session.add(detalle)
                    # Increment stock
                    insumo.stock_total_acumulado = float(insumo.stock_total_acumulado) + float(cantidad)
                
                total_compras += 1

            # Generar de 2 a 5 ventas por día
            num_ventas = random.randint(2, 5)
            for _ in range(num_ventas):
                fecha_venta = fecha_dia.replace(hour=random.randint(9, 19), minute=random.randint(0, 59))
                cliente = random.choice(clientes)

                venta = VentaEncabezado(
                    numero_pedido=f"PED-{fecha_venta.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    uuid_cliente=cliente.uuid_cliente,
                    metodo_pago=random.choice(["Tarjeta de Crédito", "Transferencia", "Efectivo", "PayPal"]),
                    estatus_envio=random.choice(["Procesando", "Enviado", "Entregado", "Completado"]),
                    fecha_venta=fecha_venta
                )
                db.session.add(venta)
                db.session.flush()

                num_detalles_venta = random.randint(1, 3)
                productos_venta = random.sample(productos, k=min(num_detalles_venta, len(productos)))

                for producto in productos_venta:
                    cantidad = random.randint(1, 4)
                    precio = producto.precio_venta
                    detalle = VentaDetalle(
                        uuid_venta=venta.uuid_venta,
                        uuid_producto=producto.uuid_producto,
                        cantidad=cantidad,
                        precio_unitario_historico=precio,
                        fecha_creacion=fecha_venta
                    )
                    db.session.add(detalle)
                    # Substract stock
                    producto.stock_fisico_actual = int(producto.stock_fisico_actual) - cantidad

                total_ventas += 1

        db.session.commit()
        print(f" [OK] {total_compras} compras históricas generadas.")
        print(f" [OK] {total_ventas} ventas históricas generadas.")
        print(">> [ÉXITO] Histórico de Transacciones completado.")

if __name__ == '__main__':
    run_seed()
