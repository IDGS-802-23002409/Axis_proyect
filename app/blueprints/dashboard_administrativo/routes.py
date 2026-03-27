from flask import render_template, flash, request
from . import dashboard_bp
from app.utils.database_connection import db
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.models.produccion import OrdenProduccion
from sqlalchemy import func
from datetime import datetime, timedelta

@dashboard_bp.route('/')
def index():
    try:
        # 1. Captura de Filtros desde la URL (GET)
        start_date_str = request.args.get('start')
        end_date_str = request.args.get('end')
        
        # Valores por defecto (Hoy)
        hoy = datetime.now().date()
        fecha_inicio = hoy
        fecha_fin = hoy

        if start_date_str and end_date_str:
            try:
                fecha_inicio = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                flash(f"Mostrando datos desde {start_date_str} hasta {end_date_str}", "info")
            except ValueError:
                flash("Formato de fecha inválido", "warning")

        # --- 2. KPI: Ventas en el Rango ---
        ventas_rango = db.session.query(
            func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
        ).join(VentaEncabezado).filter(
            func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
            func.date(VentaEncabezado.fecha_venta) <= fecha_fin
        ).scalar() or 0

        # --- 3. KPI: Unidades en el Rango ---
        unidades_rango = db.session.query(func.sum(VentaDetalle.cantidad))\
            .join(VentaEncabezado)\
            .filter(
                func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
                func.date(VentaEncabezado.fecha_venta) <= fecha_fin
            ).scalar() or 0

        # --- 4. Lógica de la Gráfica ---
        chart_labels = []
        chart_data = []
        for i in range(6, -1, -1):
            dia_t = hoy - timedelta(days=i)
            chart_labels.append(dia_t.strftime('%d %b'))
            monto = db.session.query(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
            ).join(VentaEncabezado).filter(func.date(VentaEncabezado.fecha_venta) == dia_t).scalar() or 0
            chart_data.append(float(monto))

        # --- 5. Alertas de Stock (en tiempo real) ---
        alertas_stock = db.session.query(
            ModeloRopa.nombre_modelo,
            ProductoTerminado.talla,
            ProductoTerminado.stock_fisico_actual,
            ProductoTerminado.stock_minimo_alerta
        ).join(ModeloRopa).filter(
            ProductoTerminado.stock_fisico_actual <= ProductoTerminado.stock_minimo_alerta
        ).order_by(ProductoTerminado.stock_fisico_actual.asc()).limit(5).all()

        # --- 6. Top Productos (Basado en el rango filtrado) ---
        top_productos = db.session.query(
            ModeloRopa.nombre_modelo,
            func.sum(VentaDetalle.cantidad).label('total_u')
        ).select_from(VentaDetalle)\
        .join(ProductoTerminado).join(ModeloRopa)\
        .join(VentaEncabezado).filter(
            func.date(VentaEncabezado.fecha_venta) >= fecha_inicio,
            func.date(VentaEncabezado.fecha_venta) <= fecha_fin
        ).group_by(ModeloRopa.nombre_modelo)\
        .order_by(func.sum(VentaDetalle.cantidad).desc()).limit(5).all()

        return render_template('dashboard/index.html',
                               ventas_hoy=ventas_rango,
                               unidades_24h=unidades_rango,
                               alertas_stock=alertas_stock,
                               top_productos=top_productos,
                               chart_labels=chart_labels,
                               chart_data=chart_data,
                               total_rupturas=len(alertas_stock))

    except Exception as e:
        db.session.rollback()
        flash(f"Error interno: {str(e)}", "danger")
        return render_template('dashboard/index.html')