"""
routes.py · Blueprint: ventas
Módulo de Ventas — Solo lectura
Muestra: qué se compró, cuándo, cuánto, precio total y quién compró.
"""
from flask import render_template, request, flash, redirect, url_for
from flask_security import login_required, roles_required, roles_accepted, current_user
from . import ventas_bp
from app.utils.database_connection import db
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.pedidos_cliente import PedidoClienteEncabezado, PedidoClienteDetalle
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.clientes import Cliente
from app.models.usuarios import Usuario
from app.models.produccion import OrdenProduccion
from sqlalchemy import func, or_
from datetime import datetime, timedelta
from flask_mail import Message

@ventas_bp.route('/cancelar/<uuid_venta>', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def cancelar_pedido(uuid_venta):
    venta = VentaEncabezado.query.get_or_404(uuid_venta)
    
    # REGLA: Solo se puede cancelar si el estatus es Pendiente
    if venta.estatus_envio != 'Pendiente':
        flash("Solo se pueden cancelar pedidos en estado 'Pendiente'.", "error")
        return redirect(request.referrer or url_for('ventas.index'))

    # REGLA: No hay devoluciones. Si se cancela, el producto se termina de fabricar y se integra al stock.
    # En el sistema, esto significa que la Venta se marca como Cancelada, 
    # pero las Ordenes de Producción vinculadas DEBEN continuar hasta 'Terminado'.
    # Al llegar a 'Terminado', el stock se incrementará pero ya no estará vinculado a una venta activa.
    
    venta.estatus_envio = 'Cancelado'
    db.session.commit()
    
    flash(f"Pedido {venta.numero_pedido} cancelado. La producción continuará para integrar los productos al stock.", "info")
    return redirect(request.referrer or url_for('ventas.index'))

@ventas_bp.route('/enviar/<uuid_venta>', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def marcar_enviado(uuid_venta):
    venta = VentaEncabezado.query.get_or_404(uuid_venta)
    
    # Solo si el estatus es Pendiente o Completado (no Enviado ni Cancelado)
    if venta.estatus_envio in ['Enviado', 'Cancelado']:
        flash(f"El pedido ya está en estatus {venta.estatus_envio}.", "warning")
        return redirect(url_for('ventas.index'))

    venta.estatus_envio = 'Enviado'
    db.session.commit()
    
    # Enviar correo al cliente
    try:
        from app.app import mail
        msg = Message(
            f"¡Tu pedido {venta.numero_pedido} ha sido enviado! 🚀",
            recipients=[venta.cliente.usuario.email]
        )
        msg.html = render_template(
            'emails/envio_pedido.html',
            nombre_cliente=venta.cliente.usuario.nombre_completo,
            numero_pedido=venta.numero_pedido,
            direccion=venta.cliente.direccion_completa,
            url_host=request.host_url.rstrip('/')
        )
        mail.send(msg)
        flash(f"Pedido {venta.numero_pedido} marcado como enviado y notificación enviada por correo.", "success")
    except Exception as e:
        flash(f"Pedido marcado como enviado, pero hubo un error al enviar el correo: {str(e)}", "warning")
        
    return redirect(url_for('ventas.index'))

@ventas_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():
    q          = request.args.get('q', '').strip()         
    start_str  = request.args.get('start', '')
    end_str    = request.args.get('end', '')
    estatus    = request.args.get('estatus', '')           
    page       = request.args.get('page', 1, type=int)
    per_page   = 20
    fecha_fin  = None
    fecha_ini  = None

    if start_str:
        try:
            fecha_ini = datetime.strptime(start_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    if end_str:
        try:
            fecha_fin = datetime.strptime(end_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    # ── Subconsultas para totales (Evitar duplicados por joins múltiples) ──
    # 1. Totales de Venta Directa (Stock)
    vd_sub = db.session.query(
        VentaDetalle.uuid_venta,
        func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico).label('total_vd'),
        func.sum(VentaDetalle.cantidad).label('units_vd')
    ).group_by(VentaDetalle.uuid_venta).subquery()

    # 2. Totales de Pedidos Pendientes (Producción)
    pd_sub = db.session.query(
        PedidoClienteEncabezado.uuid_venta_origen,
        func.sum(PedidoClienteDetalle.cantidad * PedidoClienteDetalle.precio_unitario_historico).label('total_pd'),
        func.sum(PedidoClienteDetalle.cantidad).label('units_pd')
    ).join(PedidoClienteDetalle, PedidoClienteEncabezado.uuid_pedido == PedidoClienteDetalle.uuid_pedido)\
     .group_by(PedidoClienteEncabezado.uuid_venta_origen).subquery()

    # ── Query principal ───────────────────────────────────────────────────
    query = (
        db.session.query(
            VentaEncabezado,
            Usuario.nombre_completo.label('nombre_cliente'),
            (func.coalesce(vd_sub.c.total_vd, 0) + func.coalesce(pd_sub.c.total_pd, 0)).label('total_venta'),
            (func.coalesce(vd_sub.c.units_vd, 0) + func.coalesce(pd_sub.c.units_pd, 0)).label('total_unidades')
        )
        .join(Cliente, VentaEncabezado.uuid_cliente == Cliente.uuid_cliente)
        .join(Usuario, Cliente.uuid_usuario == Usuario.uuid_usuario)
        .outerjoin(vd_sub, VentaEncabezado.uuid_venta == vd_sub.c.uuid_venta)
        .outerjoin(pd_sub, VentaEncabezado.uuid_venta == pd_sub.c.uuid_venta_origen)
    )
    
    if fecha_ini:
        query = query.filter(func.date(VentaEncabezado.fecha_venta) >= fecha_ini)
    if fecha_fin:
        query = query.filter(func.date(VentaEncabezado.fecha_venta) <= fecha_fin)

    # Filtro por nombre de cliente
    if q:
        query = query.filter(Usuario.nombre_completo.ilike(f'%{q}%'))

    # Filtro por estatus de envío
    if estatus:
        query = query.filter(VentaEncabezado.estatus_envio == estatus)

    query = query.order_by(VentaEncabezado.fecha_venta.desc())

    # Paginación manual
    total        = query.count()
    ventas_rows  = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages  = (total + per_page - 1) // per_page

    # ── KPIs del rango ────────────────────────────────────────────────────
    # Ajustamos KPIs para sumar ambos orígenes
    kpi_query = db.session.query(
        func.count(VentaEncabezado.uuid_venta).label('num_ventas'),
        func.sum(func.coalesce(vd_sub.c.total_vd, 0) + func.coalesce(pd_sub.c.total_pd, 0)).label('ingresos'),
        func.sum(func.coalesce(vd_sub.c.units_vd, 0) + func.coalesce(pd_sub.c.units_pd, 0)).label('unidades'),
    ).outerjoin(vd_sub, VentaEncabezado.uuid_venta == vd_sub.c.uuid_venta)\
     .outerjoin(pd_sub, VentaEncabezado.uuid_venta == pd_sub.c.uuid_venta_origen)
    
    # Aplicar mismos filtros a KPI
    if fecha_ini: kpi_query = kpi_query.filter(func.date(VentaEncabezado.fecha_venta) >= fecha_ini)
    if fecha_fin: kpi_query = kpi_query.filter(func.date(VentaEncabezado.fecha_venta) <= fecha_fin)
    if q: kpi_query = kpi_query.join(Cliente).join(Usuario).filter(Usuario.nombre_completo.ilike(f'%{q}%'))
    if estatus: kpi_query = kpi_query.filter(VentaEncabezado.estatus_envio == estatus)

    kpi = kpi_query.first()

    # ── Construir lista para el template ──────────────────────────────────
    ventas = []
    for ve, nombre_cliente, total_venta, total_unidades in ventas_rows:
        # Detalle de productos (Stock)
        productos_stock = db.session.query(
            ExplosionMaterialesCabecera.nombre_receta,
            ExplosionMaterialesCabecera.talla,
            VentaDetalle.cantidad,
            VentaDetalle.precio_unitario_historico,
        ).join(ProductoTerminado, VentaDetalle.uuid_producto == ProductoTerminado.uuid_producto)\
         .join(ExplosionMaterialesCabecera, ProductoTerminado.uuid_explosion == ExplosionMaterialesCabecera.uuid_explosion)\
         .filter(VentaDetalle.uuid_venta == ve.uuid_venta)\
         .all()

        # Detalle de productos (Pedido)
        productos_pedido = db.session.query(
            ExplosionMaterialesCabecera.nombre_receta,
            ExplosionMaterialesCabecera.talla,
            PedidoClienteDetalle.cantidad,
            PedidoClienteDetalle.precio_unitario_historico,
        ).join(PedidoClienteEncabezado, PedidoClienteDetalle.uuid_pedido == PedidoClienteEncabezado.uuid_pedido)\
         .join(ProductoTerminado, PedidoClienteDetalle.uuid_producto == ProductoTerminado.uuid_producto)\
         .join(ExplosionMaterialesCabecera, ProductoTerminado.uuid_explosion == ExplosionMaterialesCabecera.uuid_explosion)\
         .filter(PedidoClienteEncabezado.uuid_venta_origen == ve.uuid_venta)\
         .all()

        # ── Agrupar productos (Unificar Stock + Pedido) ──────────────────
        products_map = {} # (nombre, talla, precio) -> {qty, stock_qty, pedido_qty}

        for p in productos_stock:
            key = (p.nombre_receta, p.talla, float(p.precio_unitario_historico))
            if key not in products_map:
                products_map[key] = {'qty': 0, 'stock_qty': 0, 'pedido_qty': 0}
            products_map[key]['qty'] += p.cantidad
            products_map[key]['stock_qty'] += p.cantidad

        for p in productos_pedido:
            key = (p.nombre_receta, p.talla, float(p.precio_unitario_historico))
            if key not in products_map:
                products_map[key] = {'qty': 0, 'stock_qty': 0, 'pedido_qty': 0}
            products_map[key]['qty'] += p.cantidad
            products_map[key]['pedido_qty'] += p.cantidad

        combined_products = []
        for (nombre, talla, precio), data in products_map.items():
            status = "LISTO"
            if data['pedido_qty'] > 0:
                status = f"PROD ({data['pedido_qty']}/{data['qty']})"
                if data['stock_qty'] == 0:
                    status = "EN PROD"

            combined_products.append({
                'nombre' : nombre,
                'talla'  : talla,
                'qty'    : data['qty'],
                'precio' : precio,
                'status' : status
            })

        ventas.append({
            'uuid_venta'      : ve.uuid_venta,
            'numero_pedido'   : ve.numero_pedido,
            'fecha_venta'     : ve.fecha_venta,
            'cliente'         : nombre_cliente or '—',
            'metodo_pago'     : ve.metodo_pago or '—',
            'estatus_envio'   : ve.estatus_envio,
            'total_venta'     : float(total_venta or 0),
            'total_unidades'  : int(total_unidades or 0),
            'productos'       : combined_products
        })

    return render_template(
        'ventas/index.html',
        ventas        = ventas,
        kpi_ventas    = int(kpi.num_ventas   or 0),
        kpi_ingresos  = float(kpi.ingresos   or 0),
        kpi_unidades  = int(kpi.unidades     or 0),
        q             = q,
        start         = fecha_ini.strftime('%Y-%m-%d') if fecha_ini else '',
        end           = fecha_fin.strftime('%Y-%m-%d') if fecha_fin else '',
        estatus       = estatus,
        page          = page,
        total_pages   = total_pages,
        total         = total,
    )