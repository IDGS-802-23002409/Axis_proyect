"""
routes.py · Blueprint: ventas
Módulo de Ventas — Solo lectura
Muestra: qué se compró, cuándo, cuánto, precio total y quién compró.
"""
from flask import render_template, request
from flask_security import login_required, roles_required
from . import ventas_bp
from app.utils.database_connection import db
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.models.clientes import Cliente
from app.models.usuarios import Usuario
from sqlalchemy import func
from datetime import datetime, timedelta


@ventas_bp.route('/')
@login_required
@roles_required('admin', 'gerente', 'produccion')
def index():
    # ── Filtros GET ───────────────────────────────────────────────────────
    q          = request.args.get('q', '').strip()          # búsqueda por cliente
    start_str  = request.args.get('start', '')
    end_str    = request.args.get('end', '')
    estatus    = request.args.get('estatus', '')            # filtro por estatus_envio
    page       = request.args.get('page', 1, type=int)
    per_page   = 20

    # Rango de fechas por defecto: últimos 30 días
    hoy       = datetime.now().date()
    fecha_fin  = hoy
    fecha_ini  = hoy - timedelta(days=30)

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

    # ── Query principal ───────────────────────────────────────────────────
    # Une VentaEncabezado → Cliente → Usuario para obtener nombre_completo
    query = (
        db.session.query(
            VentaEncabezado,
            Usuario.nombre_completo.label('nombre_cliente'),
            func.sum(
                VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico
            ).label('total_venta'),
            func.sum(VentaDetalle.cantidad).label('total_unidades'),
        )
        .join(Cliente,     VentaEncabezado.uuid_cliente == Cliente.uuid_cliente)
        .join(Usuario,     Cliente.uuid_usuario         == Usuario.uuid_usuario)
        .join(VentaDetalle, VentaEncabezado.uuid_venta  == VentaDetalle.uuid_venta)
        .filter(
            func.date(VentaEncabezado.fecha_venta) >= fecha_ini,
            func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
        )
        .group_by(VentaEncabezado.uuid_venta, Usuario.nombre_completo)
    )

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
    kpi = db.session.query(
        func.count(func.distinct(VentaEncabezado.uuid_venta)).label('num_ventas'),
        func.sum(
            VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico
        ).label('ingresos'),
        func.sum(VentaDetalle.cantidad).label('unidades'),
    ).join(VentaDetalle, VentaEncabezado.uuid_venta == VentaDetalle.uuid_venta)\
     .filter(
         func.date(VentaEncabezado.fecha_venta) >= fecha_ini,
         func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
     ).first()

    # ── Construir lista para el template ──────────────────────────────────
    ventas = []
    for ve, nombre_cliente, total_venta, total_unidades in ventas_rows:
        # Detalle de productos de esta venta
        productos = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            VentaDetalle.cantidad,
            VentaDetalle.precio_unitario_historico,
        ).join(ProductoTerminado, VentaDetalle.uuid_producto == ProductoTerminado.uuid_producto)\
         .join(ModeloRopa,        ProductoTerminado.uuid_modelo == ModeloRopa.uuid_modelo)\
         .filter(VentaDetalle.uuid_venta == ve.uuid_venta)\
         .all()

        ventas.append({
            'uuid_venta'      : ve.uuid_venta,
            'numero_pedido'   : ve.numero_pedido,
            'fecha_venta'     : ve.fecha_venta,
            'cliente'         : nombre_cliente or '—',
            'metodo_pago'     : ve.metodo_pago or '—',
            'estatus_envio'   : ve.estatus_envio,
            'total_venta'     : float(total_venta or 0),
            'total_unidades'  : int(total_unidades or 0),
            'productos'       : [
                {
                    'nombre' : p.nombre_modelo,
                    'talla'  : p.talla,
                    'qty'    : p.cantidad,
                    'precio' : float(p.precio_unitario_historico),
                }
                for p in productos
            ],
        })

    return render_template(
        'ventas/index.html',
        ventas        = ventas,
        # KPIs
        kpi_ventas    = int(kpi.num_ventas   or 0),
        kpi_ingresos  = float(kpi.ingresos   or 0),
        kpi_unidades  = int(kpi.unidades     or 0),
        # Filtros activos
        q             = q,
        start         = fecha_ini.strftime('%Y-%m-%d'),
        end           = fecha_fin.strftime('%Y-%m-%d'),
        estatus       = estatus,
        # Paginación
        page          = page,
        total_pages   = total_pages,
        total         = total,
    )