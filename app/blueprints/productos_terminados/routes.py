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


@productos_bp.route('/registro', methods=['GET', 'POST'])
def registro_producto():
    form = ProductoTerminadoForm()

    if form.validate_on_submit():
        producto = ProductoTerminado(
            uuid_modelo=form.modelo.data,
            sku_especifico=form.sku_especifico.data.strip(),
            talla=form.talla.data,
            precio_venta=form.precio_venta.data,
            stock_fisico_actual=form.stock_fisico_actual.data,
            stock_minimo_alerta=form.stock_minimo_alerta.data,
        )
        db.session.add(producto)
        db.session.commit()

        flash('Producto terminado creado correctamente', 'success')
        return redirect(url_for('productos.index'))

    return render_template('produccion/productos_terminados/registro_producto.html', form=form)


@productos_bp.route('/editar/<uuid>', methods=['GET', 'POST'])
def editar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    form = ProductoTerminadoForm(obj=producto)

    if form.validate_on_submit():
        producto.uuid_modelo = form.modelo.data
        producto.sku_especifico = form.sku_especifico.data.strip()
        producto.talla = form.talla.data
        producto.precio_venta = form.precio_venta.data

        if form.stock_fisico_actual.data is not None:
            producto.stock_fisico_actual = form.stock_fisico_actual.data

        if form.stock_minimo_alerta.data is not None:
            producto.stock_minimo_alerta = form.stock_minimo_alerta.data

        db.session.commit()

        flash('Producto terminado actualizado correctamente', 'success')
        return redirect(url_for('productos.index'))

    # Asegurar valores existentes para evitar que se pierdan en la edición
    form.stock_fisico_actual.data = producto.stock_fisico_actual
    form.stock_minimo_alerta.data = producto.stock_minimo_alerta

    return render_template('produccion/productos_terminados/update_producto.html', form=form, producto=producto)
