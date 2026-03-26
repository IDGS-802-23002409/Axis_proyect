from flask import flash, redirect, render_template, request, url_for
from app.blueprints.productos_terminados import productos_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.utils.database_connection import db

@productos_bp.route('/productos')
def index():
    modelo_id = request.args.get('modelo', '').strip()
    talla = request.args.get('talla', '').strip()
    sku = request.args.get('sku', '').strip()
    estatus = request.args.get('estatus', '').strip()
    filtro = request.args.get('filtro', '').strip()

    productos = ProductoTerminado.query.join(ModeloRopa)

    # Filtro por estatus
    if estatus.lower() == 'activo':
        productos = productos.filter(ProductoTerminado.active.is_(True))
    elif estatus.lower() == 'inactivo':
        productos = productos.filter(ProductoTerminado.active.is_(False))
    else:
        # Por defecto mostrar solo activos
        productos = productos.filter(ProductoTerminado.active.is_(True))

    if modelo_id:
        productos = productos.filter(ProductoTerminado.uuid_modelo == modelo_id)

    if talla:
        productos = productos.filter(ProductoTerminado.talla == talla)

    if sku:
        productos = productos.filter(ProductoTerminado.sku_especifico.ilike(f"%{sku}%"))

    productos = productos.order_by(ProductoTerminado.fecha_actualizacion.desc()).all()
    
    # Calcular stats ANTES de aplicar filtros de stock (para que siempre muestren el total neto)
    total_neto = len(productos)
    en_bajo_stock_total = len([p for p in productos if p.stock_fisico_actual <= p.stock_minimo_alerta and p.stock_fisico_actual > 0])
    agotados_total = len([p for p in productos if p.stock_fisico_actual <= 0])
    
    # Aplicar filtros por stock solo a los productos mostrados
    if filtro == 'bajo_stock':
        productos = [p for p in productos if p.stock_fisico_actual <= p.stock_minimo_alerta and p.stock_fisico_actual > 0]
    elif filtro == 'agotado':
        productos = [p for p in productos if p.stock_fisico_actual <= 0]
    
    modelos = ModeloRopa.query.order_by(ModeloRopa.nombre_modelo).all()

    return render_template(
        'produccion/productos_terminados/index.html',
        productos=productos,
        total=total_neto,
        en_bajo_stock=en_bajo_stock_total,
        agotados=agotados_total,
        modelos=modelos,
        filtro_modelo=modelo_id,
        filtro_talla=talla,
        filtro_sku=sku,
        filtro_estatus=estatus,
    )


@productos_bp.route('/productos/registro', methods=['GET', 'POST'])
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


@productos_bp.route('/productos/editar/<uuid>', methods=['GET', 'POST'])
def editar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    form = ProductoTerminadoForm(obj=producto)

    if form.validate_on_submit():
        nuevo_active = bool(form.active.data)
        nuevo_stock = form.stock_fisico_actual.data if form.stock_fisico_actual.data is not None else producto.stock_fisico_actual

        if nuevo_stock > 0 and not nuevo_active:
            flash('No se puede desactivar un producto con stock físico > 0', 'error')
            return redirect(url_for('productos.editar_producto', uuid=uuid))

        producto.uuid_modelo = form.modelo.data
        producto.sku_especifico = form.sku_especifico.data.strip()
        producto.talla = form.talla.data
        producto.precio_venta = form.precio_venta.data
        producto.active = nuevo_active

        if form.stock_fisico_actual.data is not None:
            producto.stock_fisico_actual = form.stock_fisico_actual.data

        if form.stock_minimo_alerta.data is not None:
            producto.stock_minimo_alerta = form.stock_minimo_alerta.data

        db.session.commit()

        flash('Producto terminado actualizado correctamente', 'success')
        return redirect(url_for('productos.index'))

    # Cargar datos actuales en GET
    form.stock_fisico_actual.data = producto.stock_fisico_actual
    form.stock_minimo_alerta.data = producto.stock_minimo_alerta
    form.active.data = 1 if producto.active else 0

    return render_template(
        'produccion/productos_terminados/update_producto.html',
        form=form,
        producto=producto
    )

@productos_bp.route('/productos/eliminar/<uuid>', methods=['POST'])
def eliminar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)

    if producto.stock_fisico_actual > 0:
        flash('No se puede eliminar un producto con stock físico > 0', 'error')
        return redirect(url_for('productos.index'))

    producto.active = False
    db.session.commit()

    flash('Producto terminado desactivado correctamente', 'success')
    return redirect(url_for('productos.index'))


@productos_bp.route('/productos/detalle/<uuid>')
def detalle_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    modelo = producto.modelo
    
    return render_template('produccion/productos_terminados/detalle_producto.html', producto=producto, modelo=modelo)
