from flask import render_template, flash, request
from . import dashboard_bp
from app.utils.database_connection import db
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.models.produccion import OrdenProduccion
from app.models.insumos import Insumo
from sqlalchemy import func, case
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# HELPER: Sumatoria de ventas para un rango
# ─────────────────────────────────────────────
def _suma_ventas(fecha_inicio, fecha_fin):
    return db.session.query(
        func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
    ).join(VentaEncabezado).filter(
        func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
        func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
    ).scalar() or 0


# ─────────────────────────────────────────────
# HELPER: Unidades vendidas para un rango
# ─────────────────────────────────────────────
def _suma_unidades(fecha_inicio, fecha_fin):
    return db.session.query(
        func.sum(VentaDetalle.cantidad)
    ).join(VentaEncabezado).filter(
        func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
        func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
    ).scalar() or 0


# ─────────────────────────────────────────────
# ROUTE PRINCIPAL
# ─────────────────────────────────────────────
@dashboard_bp.route('/')
def index():
    try:
        hoy = datetime.now().date()
        ayer = hoy - timedelta(days=1)

        # ── 1. Parseo de filtros GET ──────────────────────────────────────
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

        # ── 2. KPI: Ventas en el rango + comparativa vs período anterior ──
        delta_dias  = (fecha_fin - fecha_inicio).days + 1
        inicio_prev = fecha_inicio - timedelta(days=delta_dias)
        fin_prev    = fecha_inicio - timedelta(days=1)

        ventas_rango = float(_suma_ventas(fecha_inicio, fecha_fin))
        ventas_prev  = float(_suma_ventas(inicio_prev, fin_prev))

        if ventas_prev > 0:
            variacion_ventas_pct = ((ventas_rango - ventas_prev) / ventas_prev) * 100
        else:
            variacion_ventas_pct = 100.0 if ventas_rango > 0 else 0.0

        tendencia_ventas = "up" if variacion_ventas_pct >= 0 else "down"

        # ── 3. KPI: Unidades en el rango + comparativa ────────────────────
        unidades_rango = int(_suma_unidades(fecha_inicio, fecha_fin))
        unidades_prev  = int(_suma_unidades(inicio_prev, fin_prev))

        if unidades_prev > 0:
            variacion_unidades_pct = ((unidades_rango - unidades_prev) / unidades_prev) * 100
        else:
            variacion_unidades_pct = 100.0 if unidades_rango > 0 else 0.0

        tendencia_unidades = "up" if variacion_unidades_pct >= 0 else "down"

        # ── 4. KPI: Órdenes de producción activas ─────────────────────────
        estados_activos = ('Pendiente', 'En Corte', 'Confección')

        ops_por_estado = db.session.query(
            OrdenProduccion.estado,
            func.count(OrdenProduccion.uuid_op).label('cantidad')
        ).filter(
            OrdenProduccion.estado.in_(estados_activos)
        ).group_by(OrdenProduccion.estado).all()

        ops_produccion = {
            'abiertas'   : sum(r.cantidad for r in ops_por_estado),
            'pendientes' : next((r.cantidad for r in ops_por_estado if r.estado == 'Pendiente'), 0),
            'en_corte'   : next((r.cantidad for r in ops_por_estado if r.estado == 'En Corte'), 0),
            'confeccion' : next((r.cantidad for r in ops_por_estado if r.estado == 'Confección'), 0),
        }

        # ── 5. KPI: Alertas de stock (productos terminados) ───────────────
        alertas_stock = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            ProductoTerminado.stock_fisico_actual,
            ProductoTerminado.stock_minimo_alerta,
        ).join(ModeloRopa).filter(
            ProductoTerminado.active == True,
            ProductoTerminado.stock_fisico_actual <= ProductoTerminado.stock_minimo_alerta,
        ).order_by(
            ProductoTerminado.stock_fisico_actual.asc()
        ).limit(5).all()

        # ── 5b. Alertas de insumos bajo mínimo ────────────────────────────
        alertas_insumos = db.session.query(
            Insumo.nombre,
            Insumo.stock_total_acumulado,
            Insumo.stock_minimo_alerta,
        ).filter(
            Insumo.stock_total_acumulado <= Insumo.stock_minimo_alerta
        ).order_by(Insumo.stock_total_acumulado.asc()).limit(5).all()

        total_rupturas = len(alertas_stock) + len(alertas_insumos)

        # ── 6. Top 5 productos más vendidos (rango filtrado) ──────────────
        top_productos = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            func.sum(VentaDetalle.cantidad).label('total_unidades'),
            func.sum(
                VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico
            ).label('total_ingresos'),
        ).select_from(VentaDetalle)\
         .join(ProductoTerminado, VentaDetalle.uuid_producto == ProductoTerminado.uuid_producto)\
         .join(ModeloRopa,        ProductoTerminado.uuid_modelo  == ModeloRopa.uuid_modelo)\
         .join(VentaEncabezado,   VentaDetalle.uuid_venta        == VentaEncabezado.uuid_venta)\
         .filter(
             func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
             func.date(VentaEncabezado.fecha_venta) <= fecha_fin,
         ).group_by(ModeloRopa.nombre_modelo, ProductoTerminado.talla)\
          .order_by(func.sum(VentaDetalle.cantidad).desc())\
          .limit(5).all()

        # ── 7. Rotación de inventario (últimos 30 días fijos) ─────────────
        hace_30 = hoy - timedelta(days=30)

        rotacion = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            ProductoTerminado.stock_fisico_actual,
            func.sum(VentaDetalle.cantidad).label('ventas_30d'),
            # días de stock restante = stock_actual / (ventas_30d / 30)
            case(
                (func.sum(VentaDetalle.cantidad) > 0,
                 (ProductoTerminado.stock_fisico_actual * 30.0) /
                 func.sum(VentaDetalle.cantidad)),
                else_=None
            ).label('dias_stock')
        ).select_from(ProductoTerminado)\
         .join(ModeloRopa, ProductoTerminado.uuid_modelo == ModeloRopa.uuid_modelo)\
         .outerjoin(VentaDetalle, ProductoTerminado.uuid_producto == VentaDetalle.uuid_producto)\
         .outerjoin(VentaEncabezado, VentaDetalle.uuid_venta == VentaEncabezado.uuid_venta)\
         .filter(
             ProductoTerminado.active == True,
             (func.date(VentaEncabezado.fecha_venta) >= hace_30) |
             (VentaEncabezado.fecha_venta == None)
         ).group_by(
             ModeloRopa.nombre_modelo,
             ProductoTerminado.talla,
             ProductoTerminado.stock_fisico_actual,
         ).order_by('dias_stock').limit(10).all()

        # ── 8. Gráfica: tendencia de ventas (últimos 7 días fijos) ────────
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

        # ── Render ─────────────────────────────────────────────────────────
        return render_template(
            'dashboard/index.html',
            # KPIs principales
            ventas_hoy            = ventas_rango,
            variacion_ventas_pct  = round(variacion_ventas_pct, 1),
            tendencia_ventas      = tendencia_ventas,
            unidades_24h          = unidades_rango,
            variacion_unidades_pct= round(variacion_unidades_pct, 1),
            tendencia_unidades    = tendencia_unidades,
            # Producción
            ops_produccion        = ops_produccion,
            # Stock
            alertas_stock         = alertas_stock,
            alertas_insumos       = alertas_insumos,
            total_rupturas        = total_rupturas,
            # Ventas
            top_productos         = top_productos,
            rotacion              = rotacion,
            # Gráfica
            chart_labels          = chart_labels,
            chart_data            = chart_data,
            # Fechas activas para el filtro
            fecha_inicio          = fecha_inicio.strftime('%Y-%m-%d'),
            fecha_fin             = fecha_fin.strftime('%Y-%m-%d'),
        )

    except Exception as e:
        db.session.rollback()
        flash(f"Error interno del servidor: {str(e)}", "danger")
        return render_template('dashboard/index.html',
                               ops_produccion={}, alertas_stock=[],
                               alertas_insumos=[], top_productos=[],
                               chart_labels=[], chart_data=[],
                               ventas_hoy=0, unidades_24h=0, total_rupturas=0)