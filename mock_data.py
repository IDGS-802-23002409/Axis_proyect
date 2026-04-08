import sys
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import random

# Asegurar que importamos desde el root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

# Importar todos los modelos para la inyección final
from app.models.usuarios import Usuario, Role
from app.models.empleados import Empleado
from app.models.clientes import Cliente
from app.models.proveedores import Proveedor
from app.models.categorias import Categoria
from app.models.modelos_productos import ModeloRopa, ProductoTerminado
from app.models.insumos import Insumo
from app.models.explosion_materiales import ExplosionMaterialesCabecera, ExplosionMaterialesDetalle
from app.models.pedidos_proveedor import PedidoProveedorEncabezado, PedidoProveedorDetalle
from app.models.compras import CompraEncabezado, CompraDetalle
from app.models.inventario import RolloInventario
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.produccion import OrdenProduccion, EjecucionCorte, MermaPiezas

def run_seed():
    with app.app_context():
        print(">> [INICIO] Iniciando inyección de datos Mock (Versión Integral)...")

        # 1. ROLES DE SEGURIDAD (Extendidos)
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

        # 2. USUARIOS Y PERFILES (Operativos y Clientes)
        test_users = [
            {"nombre": "Admin Axis", "email": "admin@axis.com", "pass": "admin1234", "role": "admin", "emp_num": "EMP-001", "puesto": "Director General", "depto": "Dirección"},
            {"nombre": "Modista Principal", "email": "modista@axis.com", "pass": "modista1234", "role": "produccion", "emp_num": "EMP-002", "puesto": "Jefe de Taller", "depto": "Producción"},
            {"nombre": "Vendedor Axis", "email": "ventas@axis.com", "pass": "ventas1234", "role": "gerente", "emp_num": "EMP-003", "puesto": "Ejecutivo Comercial", "depto": "Ventas"},
            {"nombre": "Comprador Axis", "email": "compras@axis.com", "pass": "compras1234", "role": "produccion", "emp_num": "EMP-004", "puesto": "Analista de Suministros", "depto": "Compras"},
            {"nombre": "Juan Cliente", "email": "juan@axis.com", "pass": "cliente1234", "role": "cliente", "tel": "555-123-4567", "dir": "Av. Reforma 123, CDMX"},
            {"nombre": "Maria Lopez", "email": "maria@axis.com", "pass": "cliente1234", "role": "cliente", "tel": "555-987-6543", "dir": "Insurgentes Sur 456, CDMX"}
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
                print(f" [OK] Usuario {u['email']} creado/verificado.")
        db.session.commit()

        # Helper para IDs
        admin_user = Usuario.query.filter_by(email="admin@axis.com").first()
        admin_uuid = admin_user.uuid_usuario
        cliente_obj = Cliente.query.first()
        cliente_uuid = cliente_obj.uuid_cliente

        # 3. CATEGORÍAS
        if not Categoria.query.first():
            cat_list = [
                ("Camisetas", "Prendas de cuerpo superior"),
                ("Pantalones", "Prendas inferiores"),
                ("Hoodies", "Sudaderas urbanas"),
                ("Chaquetas", "Abrigos y chamarras"),
                ("Shorts", "Pantalones cortos"),
                ("Accesorios", "Gorras y complementos")
            ]
            for n, d in cat_list:
                db.session.add(Categoria(nombre=n, descripcion=d, estatus_visible=True))
            db.session.commit()
            print(" [OK] Categorías creadas.")
        
        categorias = {c.nombre: c.uuid_categoria for c in Categoria.query.all()}

        # 4. PROVEEDORES E INSUMOS
        if not Proveedor.query.first():
            provs = [
                Proveedor(razon_social="Textiles Premium S.A.", rfc="TEX900101ABC", contacto_nombre="Elena", telefono="555-100-2000", categoria_insumo="Textiles"),
                Proveedor(razon_social="Accesorios Industriales", rfc="ACC850505XYZ", contacto_nombre="Carlos", telefono="555-300-4000", categoria_insumo="Otros"),
                Proveedor(razon_social="Hilos y Avíos del Norte", rfc="HIL220301HAN", contacto_nombre="Roberto", telefono="818-200-1010", categoria_insumo="Otros")
            ]
            db.session.add_all(provs)
            db.session.commit()
            print(" [OK] Proveedores creados.")

        prov_textiles = Proveedor.query.filter_by(razon_social="Textiles Premium S.A.").first()
        prov_accesorios = Proveedor.query.filter_by(razon_social="Accesorios Industriales").first()
        
        if not Insumo.query.first():
            ins_data = [
                {"sku": "INS-TEX-001", "nombre": "Algodón Negro Roll", "cat": "Camisetas", "med": "ROLLO", "cant": 100.0, "base": "METRO"},
                {"sku": "INS-TEX-002", "nombre": "Poliéster Gris Roll", "cat": "Hoodies", "med": "ROLLO", "cant": 50.0, "base": "METRO"},
                {"sku": "INS-TEX-003", "nombre": "Denim Azul 14oz", "cat": "Pantalones", "med": "ROLLO", "cant": 40.0, "base": "METRO"},
                {"sku": "INS-ACC-001", "nombre": "Cierre Metálico YKK 15cm", "cat": "Chaquetas", "med": "PIEZA", "cant": 1.0, "base": "PIEZA"},
                {"sku": "INS-ACC-002", "nombre": "Botón Acero Inoxidable", "cat": "Pantalones", "med": "PIEZA", "cant": 1.0, "base": "PIEZA"},
                {"sku": "INS-ACC-003", "nombre": "Etiqueta Axis Bordada", "cat": "Accesorios", "med": "PIEZA", "cant": 1.0, "base": "PIEZA"}
            ]
            for i in ins_data:
                db.session.add(Insumo(
                    sku=i["sku"],
                    nombre=i["nombre"],
                    uuid_categoria=categorias.get(i["cat"]),
                    unidad_medida=i["med"],
                    contenido_cantidad=i["cant"],
                    contenido_unidad_medida=i["base"],
                    stock_total_acumulado=0,
                    stock_minimo_alerta=10
                ))
            db.session.commit()
            print(" [OK] Insumos base creados.")

        insumos_all = Insumo.query.all()
        ins_dict = {i.sku: i.uuid_insumo for i in insumos_all}

        # 5. EXPLOSIÓN DE MATERIALES (RECETAS)
        if not ExplosionMaterialesCabecera.query.first():
            # Receta 1: Hoodie Essential
            exp1 = ExplosionMaterialesCabecera(instrucciones_proceso="Corte láser y costura reforzada.", uuid_usuario=admin_uuid, estatus='ACTIVO')
            db.session.add(exp1)
            db.session.flush()
            db.session.add_all([
                ExplosionMaterialesDetalle(uuid_explosion=exp1.uuid_explosion, uuid_insumo=ins_dict["INS-TEX-002"], consumo_teorico_unitario=2.5), 
                ExplosionMaterialesDetalle(uuid_explosion=exp1.uuid_explosion, uuid_insumo=ins_dict["INS-ACC-001"], consumo_teorico_unitario=1.0),
                ExplosionMaterialesDetalle(uuid_explosion=exp1.uuid_explosion, uuid_insumo=ins_dict["INS-ACC-003"], consumo_teorico_unitario=1.0)
            ])

            # Receta 2: T-Shirt Classic
            exp2 = ExplosionMaterialesCabecera(instrucciones_proceso="Costura plana a dos hilos.", uuid_usuario=admin_uuid, estatus='ACTIVO')
            db.session.add(exp2)
            db.session.flush()
            db.session.add_all([
                ExplosionMaterialesDetalle(uuid_explosion=exp2.uuid_explosion, uuid_insumo=ins_dict["INS-TEX-001"], consumo_teorico_unitario=1.2),
                ExplosionMaterialesDetalle(uuid_explosion=exp2.uuid_explosion, uuid_insumo=ins_dict["INS-ACC-003"], consumo_teorico_unitario=1.0)
            ])

            db.session.commit()
            print(" [OK] Recetas creadas.")

        recetas = ExplosionMaterialesCabecera.query.all()
        exp_hoodie = recetas[0]
        exp_tshirt = recetas[1]

        # 6. CATÁLOGO DE PRODUCTOS (MODELOS Y VARIANTES)
        if not ModeloRopa.query.first():
            modelos_data = [
                {"nombre": "Hoodie Oversight Black", "desc": "Sudadera pesada con fit urbano.", "cat": "Hoodies", "img": "hoodie-black.jpg", "precio": 1200.0, "sku": "H-OV-BLK", "exp": exp_hoodie.uuid_explosion},
                {"nombre": "Axis Logo Tee White", "desc": "Camiseta 100% algodón alta densidad.", "cat": "Camisetas", "img": "tshirt-white.jpg", "precio": 450.0, "sku": "T-LOG-WHT", "exp": exp_tshirt.uuid_explosion}
            ]

            for md in modelos_data:
                nuevo_mod = ModeloRopa(
                    nombre_modelo=md["nombre"],
                    descripcion=md["desc"],
                    uuid_categoria=categorias.get(md["cat"]),
                    imagen_url=f"/static/images/products/{md['img']}",
                    estatus='ACTIVO'
                )
                db.session.add(nuevo_mod)
                db.session.flush()

                for talla in ['S', 'M', 'L', 'XL']:
                    db.session.add(ProductoTerminado(
                        sku_especifico=f"{md['sku']}-{talla}",
                        uuid_modelo=nuevo_mod.uuid_modelo,
                        uuid_explosion=md["exp"],
                        talla=talla,
                        precio_venta=md["precio"],
                        stock_fisico_actual=random.randint(10, 50)
                    ))
            db.session.commit()
            print(" [OK] Catálogo de Modelos y Productos Terminados listo.")

        prod_hoodie_m = ProductoTerminado.query.filter_by(sku_especifico="H-OV-BLK-M").first()
        prod_tshirt_l = ProductoTerminado.query.filter_by(sku_especifico="T-LOG-WHT-L").first()

        # 7. COMPRAS E INVENTARIO (Poblar todos los insumos necesarios)
        if not RolloInventario.query.first():
            # Insumos a comprar
            compras_plan = [
                {"insumo": "INS-TEX-001", "prov": prov_textiles, "cant_u": 10, "m_por_u": 100.0, "costo": 150.0},
                {"insumo": "INS-TEX-002", "prov": prov_textiles, "cant_u": 5, "m_por_u": 50.0, "costo": 220.0},
                {"insumo": "INS-ACC-001", "prov": prov_accesorios, "cant_u": 100, "m_por_u": 1.0, "costo": 12.0},
                {"insumo": "INS-ACC-003", "prov": prov_accesorios, "cant_u": 500, "m_por_u": 1.0, "costo": 5.0}
            ]

            for c in compras_plan:
                ins = Insumo.query.filter_by(sku=c["insumo"]).first()
                # Pedido
                ped = PedidoProveedorEncabezado(folio_pedido=f"PED-{ins.sku}", uuid_proveedor=c["prov"].uuid_proveedor, uuid_usuario_solicita=admin_uuid, estatus='Completado')
                db.session.add(ped)
                db.session.flush()
                db.session.add(PedidoProveedorDetalle(uuid_pedido=ped.uuid_pedido, uuid_insumo=ins.uuid_insumo, cantidad_pedida=c["cant_u"], costo_unitario_estimado=c["costo"]))
                
                # Compra
                compra = CompraEncabezado(folio_factura=f"FAC-{ins.sku}-99", uuid_proveedor=c["prov"].uuid_proveedor, uuid_usuario_registro=admin_uuid, uuid_pedido=ped.uuid_pedido, estatus='RECIBIDO')
                db.session.add(compra)
                db.session.flush()
                c_det = CompraDetalle(uuid_compra=compra.uuid_compra, uuid_insumo=ins.uuid_insumo, cantidad_comprada=c["cant_u"], costo_unitario_compra=c["costo"])
                db.session.add(c_det)
                db.session.flush()

                # Inventario
                if ins.unidad_medida == 'ROLLO':
                    for _ in range(c["cant_u"]):
                        db.session.add(RolloInventario(
                            uuid_insumo=ins.uuid_insumo,
                            uuid_detalle_compra=c_det.uuid_detalle_compra,
                            metraje_inicial=c["m_por_u"],
                            metraje_continuo_actual=c["m_por_u"]
                        ))
                    ins.stock_total_acumulado = c["cant_u"] * c["m_por_u"]
                else:
                    ins.stock_total_acumulado = c["cant_u"]

            db.session.commit()
            print(" [OK] Stock inicial de todos los insumos cargado.")

        # 8. VENTAS (Múltiples órdenes para volumen)
        if not VentaEncabezado.query.first():
            ventas_data = [
                {"n": "AX-101", "cli": cliente_uuid, "m": "Tarjeta", "e": "Entregado", "prods": [(prod_hoodie_m, 1), (prod_tshirt_l, 2)]},
                {"n": "AX-102", "cli": cliente_uuid, "m": "Paypal", "e": "Procesando", "prods": [(prod_hoodie_m, 2)]}
            ]

            for vd in ventas_data:
                v_enc = VentaEncabezado(numero_pedido=vd["n"], uuid_cliente=vd["cli"], metodo_pago=vd["m"], estatus_envio=vd["e"])
                db.session.add(v_enc)
                db.session.flush()
                for p, cant in vd["prods"]:
                    db.session.add(VentaDetalle(uuid_venta=v_enc.uuid_venta, uuid_producto=p.uuid_producto, cantidad=cant, precio_unitario_historico=p.precio_venta))
            db.session.commit()
            print(" [OK] Ventas de prueba generadas.")

        # 9. PRODUCCIÓN E HISTORIAL (Cortes y Mermas)
        if not OrdenProduccion.query.first():
            v_det_hoodie = VentaDetalle.query.filter_by(cantidad=2).first()
            # OP 1: Terminada con historial
            op1 = OrdenProduccion(uuid_producto=prod_hoodie_m.uuid_producto, uuid_venta_detalle=v_det_hoodie.uuid_detalle, cantidad_a_producir=10, estado='Terminado')
            db.session.add(op1)
            db.session.flush()

            # Registro de Corte (Rollo usado)
            rollo = RolloInventario.query.filter_by(uuid_insumo=ins_dict["INS-TEX-002"]).first()
            corte = EjecucionCorte(
                uuid_op=op1.uuid_op,
                uuid_rollo_used=rollo.uuid_rollo,
                metros_teoricos_requeridos=25.0, # 10 prendas * 2.5m
                metros_sacados_bodega=26.5,
                prendas_reales_logradas=10,
                merma_real_calculada=1.5,
                usuario_corto_uuid=admin_uuid
            )
            db.session.add(corte)
            rollo.metraje_continuo_actual -= Decimal('26.5') # Descontar del rollo (simulado)

            # Registro de Merma de piezas (Accesorios)
            db.session.add(MermaPiezas(
                uuid_op=op1.uuid_op,
                uuid_insumo=ins_dict["INS-ACC-003"], # Etiquetas
                cantidad_teorica=10,
                cantidad_real_consumida=12,
                motivo='ERROR_OPERARIO',
                observaciones="2 etiquetas se dañaron al coser.",
                usuario_registro_uuid=admin_uuid
            ))

            # OP 2: Pendiente
            op2 = OrdenProduccion(uuid_producto=prod_tshirt_l.uuid_producto, cantidad_a_producir=30, estado='Pendiente')
            db.session.add(op2)

            db.session.commit()
            print(" [OK] Historial de producción y mermas inyectado.")

        print("\n>> ¡Inyección de Mock Data Finalizada con Éxito! 🎉")
        print("   - Dashboard: admin@axis.com / admin1234")
        print("   - Productor: modista@axis.com / modista1234")
        print("   - Cliente: juan@axis.com / cliente1234")

if __name__ == '__main__':
    run_seed()

