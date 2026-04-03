from flask import flash, redirect, render_template, request, url_for
from app.blueprints.productos_terminados import productos_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.utils.database_connection import db

@productos_bp.route('/')
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
        filtro_stock=filtro,
    )


from app.models.explosion_materiales import ExplosionMaterialesCabecera

@productos_bp.route('/registro', methods=['GET', 'POST'])
def registro_producto():
    form = ProductoTerminadoForm()

    
    explosiones = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').all()

    data_explosiones = []
    for e in explosiones:
        detalles = []
        for d in e.detalles:
            detalles.append({
                "insumo": d.insumo.nombre,
                "consumo": float(d.consumo_teorico_unitario)
            })

        data_explosiones.append({
            "id": e.uuid_explosion,
            "detalles": detalles
        })

    if form.validate_on_submit():
        try:
            sku = form.sku_especifico.data.strip()

            existe = ProductoTerminado.query.filter_by(
                sku_especifico=sku
            ).first()

            if existe:
                flash('El SKU ya existe', 'error')
                return render_template(
                    'produccion/productos_terminados/registro_producto.html',
                    form=form,
                    explosiones_data=data_explosiones
                )

            producto = ProductoTerminado(
                uuid_modelo=form.modelo.data,
                uuid_explosion=form.explosion.data,
                sku_especifico=sku,
                talla=form.talla.data,
                precio_venta=float(form.precio_venta.data),
                stock_fisico_actual=0,
                stock_minimo_alerta=form.stock_minimo_alerta.data or 0,
                active=bool(form.active.data)
            )

            db.session.add(producto)
            db.session.commit()

            flash('Producto terminado creado correctamente', 'success')
            return redirect(url_for('productos_bp.index'))

        except Exception as e:
            db.session.rollback()
            print("ERROR:", e)
            flash('Error al crear el producto', 'error')

    return render_template(
        'produccion/productos_terminados/registro_producto.html',
        form=form,
        explosiones_data=data_explosiones  
    )

@productos_bp.route('/editar/<uuid>', methods=['GET', 'POST'])
def editar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    form = ProductoTerminadoForm(obj=producto)

    if form.validate_on_submit():
        nuevo_sku = form.sku_especifico.data.strip()

        # Validar SKU duplicado
        sku_duplicado = ProductoTerminado.query.filter(
            ProductoTerminado.sku_especifico == nuevo_sku,
            ProductoTerminado.uuid_producto != producto.uuid_producto
        ).first()

        if sku_duplicado:
            flash('El SKU ya existe en otro producto', 'error')
            return redirect(url_for('productos.editar_producto', uuid=uuid))

        # Actualizar datos (SIN stock)
        producto.uuid_modelo = form.modelo.data
        producto.sku_especifico = nuevo_sku
        producto.talla = form.talla.data
        producto.precio_venta = form.precio_venta.data
        producto.active = bool(form.active.data)

        # Solo mínimo alerta (opcional)
        if form.stock_minimo_alerta.data is not None:
            producto.stock_minimo_alerta = form.stock_minimo_alerta.data

        db.session.commit()

        flash('Producto terminado actualizado correctamente', 'success')
        return redirect(url_for('productos_bp.index'))

    # Cargar datos en GET (SIN stock físico)
    form.stock_minimo_alerta.data = producto.stock_minimo_alerta
    form.active.data = 1 if producto.active else 0

    return render_template(
        'produccion/productos_terminados/update_producto.html',
        form=form,
        producto=producto
    )

@productos_bp.route('/eliminar/<uuid>', methods=['POST'])
def eliminar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)

    producto.active = False
    db.session.commit()

    flash('Producto terminado desactivado correctamente', 'success')
    return redirect(url_for('productos_bp.index'))


@productos_bp.route('/detalle/<uuid>')
def detalle_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    modelo = producto.modelo
    
    return render_template('produccion/productos_terminados/detalle_producto.html', producto=producto, modelo=modelo)
