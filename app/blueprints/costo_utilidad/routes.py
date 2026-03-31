from flask import render_template, request, redirect, url_for, flash
from app.blueprints.costo_utilidad import costo_utilidad_bp
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera, ExplosionMaterialesDetalle
from app.models.insumos import Insumo
from flask_security import login_required, roles_required
from app.utils.database_connection import db


def _calcular_costo_mp(producto):
    cabecera = ExplosionMaterialesCabecera.query.filter_by(uuid_producto=producto.uuid_producto).first()
    if not cabecera:
        return 0.0

    detalles = ExplosionMaterialesDetalle.query.filter_by(uuid_explosion=cabecera.uuid_explosion).all()
    if not detalles:
        return 0.0

    costo_mp = 0.0
    for d in detalles:
        insumo = Insumo.query.filter_by(uuid_insumo=d.uuid_insumo).first()
        if insumo and insumo.costo_unitario_individual is not None:
            costo_mp += float(d.consumo_teorico_unitario or 0) * float(insumo.costo_unitario_individual or 0)
    return costo_mp


@costo_utilidad_bp.route('/costo-utilidad', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def index():
    productos = ProductoTerminado.query.order_by(ProductoTerminado.fecha_actualizacion.desc()).all()

    product = None
    costo_mp = 0.0
    costo_produccion = 0.0
    margen = 0.0
    costo_total = 0.0
    utilidad_actual = 0.0
    precio_ajustado = 0.0

    if request.method == 'GET':
        uuid_producto = request.args.get('producto', '').strip()
        if uuid_producto:
            product = ProductoTerminado.query.filter_by(uuid_producto=uuid_producto).first()

    if request.method == 'POST':
        uuid_producto = request.form.get('producto').strip()
        product = ProductoTerminado.query.filter_by(uuid_producto=uuid_producto).first()

        if not product:
            flash('Producto no encontrado.', 'error')
            return redirect(url_for('costo_utilidad.index'))

        try:
            costo_produccion = float(request.form.get('costo_produccion', 0) or 0)
        except ValueError:
            costo_produccion = 0.0

        try:
            margen = float(request.form.get('margen', 0) or 0)
        except ValueError:
            margen = 0.0

        costo_mp = _calcular_costo_mp(product)
        costo_total = costo_mp + costo_produccion

        try:
            precio_actual = float(product.precio_venta or 0)
        except (TypeError, ValueError):
            precio_actual = 0.0

        if costo_total > 0:
            utilidad_actual = ((precio_actual - costo_total) / costo_total) * 100
        else:
            utilidad_actual = 0.0

        precio_ajustado = costo_total * (1 + (margen / 100))

        if request.form.get('guardar_precio') == '1':
            product.precio_venta = precio_ajustado
            db.session.commit()
            flash(f'Precio actualizado a ${precio_ajustado:.2f} para {product.sku_especifico}', 'success')

    # si el usuario solo seleccionó producto (GET), traer cálculo base con costo de materia prima
    if request.method == 'GET' and product:
        costo_mp = _calcular_costo_mp(product)

    return render_template(
        'produccion/costo_utilidad/index.html',
        productos=productos,
        producto=product,
        costo_mp=costo_mp,
        costo_produccion=costo_produccion,
        margen=margen,
        costo_total=costo_total,
        utilidad_actual=utilidad_actual,
        precio_ajustado=precio_ajustado,
    )
