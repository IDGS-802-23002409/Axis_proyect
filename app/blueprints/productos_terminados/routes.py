from flask import flash, redirect, render_template, request, url_for
from app.blueprints.productos_terminados import productos_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.utils.database_connection import db

@productos_bp.route('/')
def index():
    modelo_id = request.args.get('modelo', '').strip()
    talla = request.args.get('talla', '').strip()

    productos = ProductoTerminado.query.join(ModeloRopa)

    if modelo_id:
        productos = productos.filter(ProductoTerminado.uuid_modelo == modelo_id)

    if talla:
        productos = productos.filter(ProductoTerminado.talla == talla)

    productos = productos.order_by(ProductoTerminado.fecha_actualizacion.desc()).all()
    total = len(productos)
    en_bajo_stock = len([p for p in productos if p.stock_fisico_actual <= p.stock_minimo_alerta])
    agotados = len([p for p in productos if p.stock_fisico_actual <= 0])
    modelos = ModeloRopa.query.order_by(ModeloRopa.nombre_modelo).all()

    return render_template(
        'produccion/productos_terminados/index.html',
        productos=productos,
        total=total,
        en_bajo_stock=en_bajo_stock,
        agotados=agotados,
        modelos=modelos,
        filtro_modelo=modelo_id,
        filtro_talla=talla,
    )
