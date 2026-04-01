from flask import render_template, request, redirect, url_for, flash
from app.blueprints.costo_utilidad import costo_utilidad_bp
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera, ExplosionMaterialesDetalle
from app.models.insumos import Insumo
from app.models.compras import CompraEncabezado, CompraDetalle
from flask_security import login_required, roles_required
from app.utils.database_connection import db


def _obtener_costo_promedio_insumo(uuid_insumo):
    """
    Calcula el costo promedio ponderado por UNIDAD BASE
    usando las últimas 5 compras del insumo.

    Fórmula:
        total gastado / total unidades base compradas
    """
    detalles = (
        CompraDetalle.query
        .filter_by(uuid_insumo=uuid_insumo)
        .join(CompraEncabezado)
        .order_by(CompraEncabezado.fecha_compra.desc())
        .limit(5)
        .all()
    )

    if not detalles:
        return 0.0

    total_costo = 0.0
    total_unidades_base = 0.0

    for d in detalles:
        if (
            d.costo_unitario_compra is not None and
            d.cantidad_comprada is not None and
            d.insumo is not None and
            d.insumo.contenido_cantidad is not None and
            float(d.insumo.contenido_cantidad) > 0
        ):
            cantidad_comprada = float(d.cantidad_comprada)
            costo_unitario_compra = float(d.costo_unitario_compra)
            contenido_cantidad = float(d.insumo.contenido_cantidad)

            total_costo += cantidad_comprada * costo_unitario_compra
            total_unidades_base += cantidad_comprada * contenido_cantidad

    if total_unidades_base == 0:
        return 0.0

    return total_costo / total_unidades_base


def _obtener_explosion_y_detalles(producto):
    """
    Obtiene la cabecera y los detalles de explosión de materiales del producto.
    """
    cabecera = ExplosionMaterialesCabecera.query.filter_by(
        uuid_producto=producto.uuid_producto
    ).first()

    if not cabecera:
        return None, []

    detalles = ExplosionMaterialesDetalle.query.filter_by(
        uuid_explosion=cabecera.uuid_explosion
    ).all()

    return cabecera, detalles


def _calcular_costo_mp(producto):
    """
    Calcula el costo total de materia prima del producto.
    """
    _, detalles = _obtener_explosion_y_detalles(producto)

    if not detalles:
        return 0.0

    costo_mp = 0.0

    for d in detalles:
        insumo = Insumo.query.filter_by(uuid_insumo=d.uuid_insumo).first()
        if not insumo:
            continue

        costo_promedio = _obtener_costo_promedio_insumo(insumo.uuid_insumo)
        consumo = float(d.consumo_teorico_unitario or 0)

        costo_mp += consumo * costo_promedio

    return costo_mp


def _obtener_desglose_insumos(producto):
    """
    Devuelve el desglose de insumos del producto con:
    - nombre del insumo
    - consumo teórico unitario
    - costo promedio por unidad base
    - costo total del insumo en el producto
    """
    _, detalles = _obtener_explosion_y_detalles(producto)

    if not detalles:
        return []

    desglose = []

    for d in detalles:
        insumo = Insumo.query.filter_by(uuid_insumo=d.uuid_insumo).first()
        if not insumo:
            continue

        costo_promedio = _obtener_costo_promedio_insumo(insumo.uuid_insumo)
        consumo = float(d.consumo_teorico_unitario or 0)
        costo_total_insumo = consumo * costo_promedio

        desglose.append({
            'insumo': insumo.nombre if insumo.nombre else 'N/A',
            'unidad_base': insumo.contenido_unidad_medida,
            'consumo': consumo,
            'costo_unitario': costo_promedio,
            'costo_total': costo_total_insumo,
        })

    return desglose

# @costo_utilidad_bp.route('/costo-utilidad', methods=['GET'])
# @login_required
# @roles_required('admin')
# def index():
#     productos = ProductoTerminado.query.order_by(
#         ProductoTerminado.modelo_id,
#         ProductoTerminado.talla
#     ).all()

#     return render_template(
#         'produccion/costo_utilidad/index.html',
#         productos=productos,
#     )


@costo_utilidad_bp.route('/costo-utilidad', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def index():
    productos = ProductoTerminado.query.order_by(
        ProductoTerminado.fecha_actualizacion.desc()
    ).all()

    product = None
    costo_mp = 0.0
    margen = 0.0
    utilidad_actual = 0.0
    precio_ajustado = 0.0
    desglose_insumos = []

    # ----------------------------
    # GET: Selección de producto
    # ----------------------------
    if request.method == 'GET':
        uuid_producto = (request.args.get('producto') or '').strip()

        if uuid_producto:
            product = ProductoTerminado.query.filter_by(
                uuid_producto=uuid_producto
            ).first()

            if product:
                _, detalles = _obtener_explosion_y_detalles(product)
                costo_mp = _calcular_costo_mp(product)
                desglose_insumos = _obtener_desglose_insumos(product)

                if not detalles:
                    flash(
                        'Este producto no tiene explosión de materiales configurada.',
                        'warning'
                    )
                elif costo_mp == 0.0:
                    flash(
                        'No fue posible calcular el costo del producto. Verifica compras, contenido del insumo y consumos configurados.',
                        'warning'
                    )
                    
    if request.method == 'POST':
        uuid_producto = (request.form.get('producto') or '').strip()

        product = ProductoTerminado.query.filter_by(
            uuid_producto=uuid_producto
        ).first()

        if not product:
            flash('Producto no encontrado.', 'error')
            return redirect(url_for('costo_utilidad.index'))

        try:
            margen = float(request.form.get('margen', 0) or 0)
        except ValueError:
            margen = 0.0

        _, detalles = _obtener_explosion_y_detalles(product)
        costo_mp = _calcular_costo_mp(product)
        desglose_insumos = _obtener_desglose_insumos(product)

        if not detalles:
            flash(
                'Este producto no tiene explosión de materiales configurada.',
                'error'
            )
            return redirect(url_for('costo_utilidad.index', producto=product.uuid_producto))

        if costo_mp == 0.0:
            flash(
                'No fue posible calcular el costo del producto. Verifica compras, contenido del insumo y consumos configurados.',
                'error'
            )
            return redirect(url_for('costo_utilidad.index', producto=product.uuid_producto))

        try:
            precio_actual = float(product.precio_venta or 0)
        except (TypeError, ValueError):
            precio_actual = 0.0

        if costo_mp > 0:
            utilidad_actual = ((precio_actual - costo_mp) / costo_mp) * 100
        else:
            utilidad_actual = 0.0

        precio_ajustado = costo_mp * (1 + (margen / 100))

        if request.form.get('guardar_precio') == '1':
            product.precio_venta = precio_ajustado
            db.session.commit()

            flash(
                f'Precio actualizado a ${precio_ajustado:.2f} para {product.sku_especifico}',
                'success'
            )

            return redirect(url_for('costo_utilidad.index', producto=product.uuid_producto))

    return render_template(
        'produccion/costo_utilidad/index.html',
        productos=productos,
        producto=product,
        costo_mp=costo_mp,
        margen=margen,
        utilidad_actual=utilidad_actual,
        precio_ajustado=precio_ajustado,
        desglose_insumos=desglose_insumos,
    )