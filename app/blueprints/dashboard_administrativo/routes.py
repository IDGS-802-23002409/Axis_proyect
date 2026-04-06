from flask import render_template, flash, request
from flask_security import login_required, roles_required, roles_accepted
from . import dashboard_bp
from app.utils.database_connection import db
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.models.produccion import OrdenProduccion
from app.models.insumos import Insumo
from sqlalchemy import func, case
from datetime import datetime, timedelta


def _suma_ventas(fecha_inicio, fecha_fin):
    return db.session.query(
        func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
    ).join(VentaEncabezado).filter(
        func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
        func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
    ).scalar() or 0


def _suma_unidades(fecha_inicio, fecha_fin):
    return db.session.query(
        func.sum(VentaDetalle.cantidad)
    ).join(VentaEncabezado).filter(
        func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
        func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
    ).scalar() or 0


@dashboard_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente')
def index():
    try:
        hoy  = datetime.now().date()
        ayer = hoy - timedelta(days=1)

        # ── 1. Filtros GET ────────────────────────────────────────────────
        start_str = request.args.get('start')
        end_str   = request.args.get('end')

        fecha_inicio = hoy
        fecha_fin    = hoy

        if start_str and end_str:
            try:
                fecha_inicio = datetime.strptime(start_str, '%Y-%m-%d').date()
                fecha_fin    = datetime.strptime(end_str,   '%Y-%m-%d').date()
                if fecha_inicio > fecha_fin:
                    raise ValueError("Rango inválido")
            except ValueError as exc:
                flash(f"Fechas incorrectas: {exc}", "warning")
                fecha_inicio = fecha_fin = hoy

        # ── 2. KPI Ventas + comparativa ───────────────────────────────────
        delta_dias  = (fecha_fin - fecha_inicio).days + 1
        inicio_prev = fecha_inicio - timedelta(days=delta_dias)
        fin_prev    = fecha_inicio - timedelta(days=1)

        ventas_rango = float(_suma_ventas(fecha_inicio, fecha_fin))
        ventas_prev  = float(_suma_ventas(inicio_prev, fin_prev))

        variacion_ventas_pct = (
            ((ventas_rango - ventas_prev) / ventas_prev) * 100
            if ventas_prev > 0 else (100.0 if ventas_rango > 0 else 0.0)
        )
        tendencia_ventas = "up" if variacion_ventas_pct >= 0 else "down"

        # ── 3. KPI Unidades + comparativa ─────────────────────────────────
        unidades_rango = int(_suma_unidades(fecha_inicio, fecha_fin))
        unidades_prev  = int(_suma_unidades(inicio_prev, fin_prev))

        variacion_unidades_pct = (
            ((unidades_rango - unidades_prev) / unidades_prev) * 100
            if unidades_prev > 0 else (100.0 if unidades_rango > 0 else 0.0)
        )
        tendencia_unidades = "up" if variacion_unidades_pct >= 0 else "down"

        # ── 4. KPI Órdenes de producción ──────────────────────────────────
        estados_activos = ('Pendiente', 'En Corte', 'Confección')
        ops_por_estado  = db.session.query(
            OrdenProduccion.estado,
            func.count(OrdenProduccion.uuid_op).label('cantidad')
        ).filter(OrdenProduccion.estado.in_(estados_activos))\
         .group_by(OrdenProduccion.estado).all()

        ops_produccion = {
            'abiertas'  : sum(r.cantidad for r in ops_por_estado),
            'pendientes': next((r.cantidad for r in ops_por_estado if r.estado == 'Pendiente'), 0),
            'en_corte'  : next((r.cantidad for r in ops_por_estado if r.estado == 'En Corte'), 0),
            'confeccion': next((r.cantidad for r in ops_por_estado if r.estado == 'Confección'), 0),
        }

        # ── 5. Alertas de stock — SIN filtro active ────────────────────────
        alertas_stock = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            ProductoTerminado.stock_fisico_actual,
            ProductoTerminado.stock_minimo_alerta,
        ).join(ModeloRopa).filter(
            ProductoTerminado.stock_fisico_actual <= ProductoTerminado.stock_minimo_alerta,
        ).order_by(ProductoTerminado.stock_fisico_actual.asc()).limit(5).all()

        # ── 5b. Alertas de insumos ─────────────────────────────────────────
        alertas_insumos = db.session.query(
            Insumo.nombre,
            Insumo.stock_total_acumulado,
            Insumo.stock_minimo_alerta,
        ).filter(
            Insumo.stock_total_acumulado <= Insumo.stock_minimo_alerta
        ).order_by(Insumo.stock_total_acumulado.asc()).limit(5).all()

        total_rupturas = len(alertas_stock) + len(alertas_insumos)

        # ── 6. Top 5 productos más vendidos ───────────────────────────────
        top_productos_raw = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            func.sum(VentaDetalle.cantidad).label('total_unidades'),
            func.sum(
                VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico
            ).label('total_ingresos'),
        ).select_from(VentaDetalle)\
         .join(ProductoTerminado, VentaDetalle.uuid_producto == ProductoTerminado.uuid_producto)\
         .join(ModeloRopa,        ProductoTerminado.uuid_modelo == ModeloRopa.uuid_modelo)\
         .join(VentaEncabezado,   VentaDetalle.uuid_venta == VentaEncabezado.uuid_venta)\
         .filter(
             func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
             func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
         ).group_by(ModeloRopa.nombre_modelo, ProductoTerminado.talla)\
          .order_by(func.sum(VentaDetalle.cantidad).desc())\
          .limit(5).all()

        top_productos = top_productos_raw  # lista para tabla

        # ── 7. Top producto y bottom producto (para las cards) ─────────────
        # Período extendido: últimos 30 días para tener más datos
        hace_30 = hoy - timedelta(days=30)

        ranking_completo = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            ProductoTerminado.stock_fisico_actual,
            func.coalesce(func.sum(VentaDetalle.cantidad), 0).label('total_vendido'),
            func.coalesce(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico), 0
            ).label('total_monto'),
        ).select_from(ProductoTerminado)\
         .join(ModeloRopa, ProductoTerminado.uuid_modelo == ModeloRopa.uuid_modelo)\
         .outerjoin(VentaDetalle,   ProductoTerminado.uuid_producto == VentaDetalle.uuid_producto)\
         .outerjoin(VentaEncabezado, VentaDetalle.uuid_venta == VentaEncabezado.uuid_venta)\
         .filter(
             (func.date(VentaEncabezado.fecha_venta) >= hace_30) |
             (VentaEncabezado.fecha_venta == None)
         ).group_by(
             ModeloRopa.nombre_modelo,
             ProductoTerminado.talla,
             ProductoTerminado.stock_fisico_actual,
         ).order_by(func.coalesce(func.sum(VentaDetalle.cantidad), 0).desc())\
          .all()

        top_producto    = None
        bottom_producto = None

        if ranking_completo:
            t = ranking_completo[0]
            top_producto = {
                'nombre'  : f"{t.nombre_modelo} · {t.talla}",
                'unidades': int(t.total_vendido),
                'monto'   : float(t.total_monto),
                'imagen'  : None,
            }
            b = ranking_completo[-1]
            bottom_producto = {
                'nombre' : f"{b.nombre_modelo} · {b.talla}",
                'stock'  : int(b.stock_fisico_actual or 0),
                'imagen' : None,
            }

        # ── 8. Gráfica: últimos 7 días ────────────────────────────────────
        chart_labels = []
        chart_data   = []

        for i in range(6, -1, -1):
            dia = hoy - timedelta(days=i)
            chart_labels.append(dia.strftime('%d %b'))
            monto = db.session.query(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
            ).join(VentaEncabezado)\
             .filter(func.date(VentaEncabezado.fecha_venta) == dia)\
             .scalar() or 0
            chart_data.append(float(monto))

        return render_template(
            'dashboard/index.html',
            ventas_hoy             = ventas_rango,
            variacion_ventas_pct   = round(variacion_ventas_pct, 1),
            tendencia_ventas       = tendencia_ventas,
            unidades_24h           = unidades_rango,
            variacion_unidades_pct = round(variacion_unidades_pct, 1),
            tendencia_unidades     = tendencia_unidades,
            ops_produccion         = ops_produccion,
            alertas_stock          = alertas_stock,
            alertas_insumos        = alertas_insumos,
            total_rupturas         = total_rupturas,
            top_productos          = top_productos,
            top_producto           = top_producto,
            bottom_producto        = bottom_producto,
            rotacion               = [],
            chart_labels           = chart_labels,
            chart_data             = chart_data,
            fecha_inicio           = fecha_inicio.strftime('%Y-%m-%d'),
            fecha_fin              = fecha_fin.strftime('%Y-%m-%d'),
        )

    except Exception as e:
        db.session.rollback()
        flash(f"Error interno: {str(e)}", "danger")
        return render_template(
            'dashboard/index.html',
            ops_produccion={}, alertas_stock=[], alertas_insumos=[],
            top_productos=[], top_producto=None, bottom_producto=None,
            chart_labels=[], chart_data=[],
            ventas_hoy=0, unidades_24h=0, total_rupturas=0, rotacion=[],
        )