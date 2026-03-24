from flask import render_template, jsonify, abort
from . import dashboard_bp
from app.models.proveedores import Proveedor 
import models
from app.utils.database_connection import db
from sqlalchemy import func, text
from datetime import datetime

@dashboard_bp.route('/')
def index():
    hoy = datetime.now().date()
    
    # 1. TOTAL VENTAS DIARIAS 
    # Se suma (cantidad * precio_historico) de los detalles de hoy
    ventas_hoy = db.session.query(
        func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
    ).join(VentaEncabezado).filter(func.date(VentaEncabezado.fecha_venta) == hoy).scalar() or 0

    tickets = VentaEncabezado.query.filter(func.date(VentaEncabezado.fecha_venta) == hoy).count()
    
    unidades = db.session.query(func.sum(VentaDetalle.cantidad)).join(VentaEncabezado)\
        .filter(func.date(VentaEncabezado.fecha_venta) == hoy).scalar() or 0

    rupturas_count = Insumo.query.filter(Insumo.stock_total_acumulado <= Insumo.stock_minimo_alerta).count()

    # 2. TOP PRODUCTOS VENDIDOS
    top_productos = db.session.query(
        ProductoTerminado.nombre_producto,
        func.sum(VentaDetalle.cantidad).label('total')
    ).join(VentaDetalle).join(VentaEncabezado)\
     .filter(func.date(VentaEncabezado.fecha_venta) == hoy)\
     .group_by(ProductoTerminado.uuid_producto)\
     .order_by(text('total DESC')).limit(4).all()

    # 3. ALERTAS DE STOCK 
    alertas_insumos = Insumo.query.filter(Insumo.stock_total_acumulado <= Insumo.stock_minimo_alerta * 1.2)\
        .order_by(Insumo.stock_total_acumulado.asc()).limit(4).all()

    pulse = {
        "ventas": ventas_hoy,
        "tickets": tickets,
        "unidades": unidades,
        "rupturas": rupturas_count,
        "rotacion": "2.7x" 
    }

    return render_template('/index.html', pulse=pulse, productos=top_productos, alertas=alertas_insumos)