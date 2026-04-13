import os
import uuid as uuid_lib
from flask import current_app, flash, redirect, render_template, request, url_for
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from app.blueprints.productos_terminados import productos_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.utils.database_connection import db
from flask_security import login_required, roles_accepted

def get_upload_folder():
    """Garantiza la existencia y retorna la ruta local de las fotos de modelos."""
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'modelos')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder


@productos_bp.route('/')
@login_required
@roles_accepted('admin', 'produccion')
def index():
    explosion_id = request.args.get('explosion', '').strip()
    talla = request.args.get('talla', '').strip()
    sku = request.args.get('sku', '').strip()
    estatus = request.args.get('estatus', '').strip()
    filtro = request.args.get('filtro', '').strip()

    productos = ProductoTerminado.query.join(ExplosionMaterialesCabecera)

    # Filtro por estatus
    if estatus.lower() == 'activo':
        productos = productos.filter(ProductoTerminado.active.is_(True))
    elif estatus.lower() == 'inactivo':
        productos = productos.filter(ProductoTerminado.active.is_(False))
    else:
        # Por defecto mostrar solo activos
        productos = productos.filter(ProductoTerminado.active.is_(True))

    if explosion_id:
        productos = productos.filter(ProductoTerminado.uuid_explosion == explosion_id)

    if talla:
        productos = productos.filter(ExplosionMaterialesCabecera.talla == talla)

    if sku:
        productos = productos.filter(ProductoTerminado.sku_especifico.ilike(f"%{sku}%"))

    productos = productos.order_by(
    ExplosionMaterialesCabecera.nombre_receta,
    ExplosionMaterialesCabecera.talla
).all()
    
    # Calcular stats ANTES de aplicar filtros de stock
    todos_productos_activos = ProductoTerminado.query.filter_by(active=True).all()
    total_neto = len(todos_productos_activos)
    en_bajo_stock_total = len([p for p in todos_productos_activos if p.stock_fisico_actual <= p.stock_minimo_alerta and p.stock_fisico_actual > 0])
    agotados_total = len([p for p in todos_productos_activos if p.stock_fisico_actual <= 0])
    
    # Aplicar filtros por stock solo a los productos mostrados
    if filtro == 'bajo_stock':
        productos = [p for p in productos if p.stock_fisico_actual <= p.stock_minimo_alerta and p.stock_fisico_actual > 0]
    elif filtro == 'agotado':
        productos = [p for p in productos if p.stock_fisico_actual <= 0]
    
    # Obtener explosiones activas para el dropdown
    explosiones = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').order_by(ExplosionMaterialesCabecera.nombre_receta).all()

    return render_template(
        'produccion/productos_terminados/index.html',
        productos=productos,
        total=total_neto,
        en_bajo_stock=en_bajo_stock_total,
        agotados=agotados_total,
        explosiones=explosiones,
        filtro_explosion=explosion_id,
        filtro_talla=talla,
        filtro_sku=sku,
        filtro_estatus=estatus,
        filtro_stock=filtro,
    )

@productos_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'produccion')
def registro_producto():
    form = ProductoTerminadoForm()
    subquery = db.session.query(ProductoTerminado.uuid_explosion)

    explosiones = ExplosionMaterialesCabecera.query.filter(
        ExplosionMaterialesCabecera.estatus == 'ACTIVO',
        ~ExplosionMaterialesCabecera.uuid_explosion.in_(subquery)
    ).all()
    form.explosion.choices = [
        (str(e.uuid_explosion), f"{e.nombre_receta} Talla {e.talla}")
        for e in explosiones
    ]

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
                
            imagen_url = "/static/images/default/default-image.png"
        
            # Procesamiento de la imagen
            if form.imagen.data:
                file = form.imagen.data
                filename = secure_filename(f"{uuid_lib.uuid4().hex}_{file.filename}")
                filepath = os.path.join(get_upload_folder(), filename)
                file.save(filepath)
                # Guardar la url parcial estática esperada por el navegador
                imagen_url = f"/static/uploads/modelos/{filename}"

            producto = ProductoTerminado(
                uuid_explosion=form.explosion.data,
                sku_especifico=sku,
                precio_venta=float(form.precio_venta.data),
                stock_fisico_actual=0,
                stock_minimo_alerta=form.stock_minimo_alerta.data or 0,
                active=bool(form.active.data),
                imagen_url=imagen_url
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
@login_required
@roles_accepted('admin', 'produccion')
def editar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    form = ProductoTerminadoForm(obj=producto)

    # Cargar explosiones para el script de previsualización
    subquery = db.session.query(ProductoTerminado.uuid_explosion).filter(
    ProductoTerminado.uuid_producto != producto.uuid_producto
)

    explosiones = ExplosionMaterialesCabecera.query.filter(
    ExplosionMaterialesCabecera.estatus == 'ACTIVO',
    or_(
        ExplosionMaterialesCabecera.uuid_explosion == producto.uuid_explosion,
        ~ExplosionMaterialesCabecera.uuid_explosion.in_(subquery)
    )
).all()
    form.explosion.choices = [
    (str(e.uuid_explosion), f"{e.nombre_receta} Talla {e.talla}")
    for e in explosiones
]
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
        nuevo_sku = form.sku_especifico.data.strip()

        # Validar SKU duplicado
        sku_duplicado = ProductoTerminado.query.filter(
            ProductoTerminado.sku_especifico == nuevo_sku,
            ProductoTerminado.uuid_producto != producto.uuid_producto
        ).first()

        if sku_duplicado:
            flash('El SKU ya existe en otro producto', 'error')
            return render_template(
                'produccion/productos_terminados/update_producto.html',
                form=form,
                producto=producto,
                explosiones_data=data_explosiones
            )

        # NUEVO: Validar si se intenta cambiar la receta y hay órdenes activas
        if form.explosion.data != producto.uuid_explosion:
            from app.models.produccion import OrdenProduccion
            ordenes_activas = OrdenProduccion.query.filter(
                OrdenProduccion.uuid_producto == producto.uuid_producto,
                OrdenProduccion.estado != 'Terminado'
            ).first()
            
            if ordenes_activas:
                flash('No se puede cambiar la receta porque existen órdenes de producción activas para este producto.', 'error')
                return render_template(
                    'produccion/productos_terminados/update_producto.html',
                    form=form,
                    producto=producto,
                    explosiones_data=data_explosiones
                )

        # Actualizar datos (SIN stock, SIN uuid_modelo, SIN talla - vienen de la explosión)
        producto.uuid_explosion = form.explosion.data
        producto.sku_especifico = nuevo_sku
        producto.precio_venta = form.precio_venta.data
        producto.active = True if form.active.data == 1 else False

        # Solo mínimo alerta (opcional)
        if form.stock_minimo_alerta.data is not None:
            producto.stock_minimo_alerta = form.stock_minimo_alerta.data
        file = request.files.get('imagen')
        if file and file.filename:
            if file.filename != '':
                filename = secure_filename(f"{uuid_lib.uuid4().hex}_{file.filename}")
                filepath = os.path.join(get_upload_folder(), filename)
                file.save(filepath)
                    # Opcionalmente podrías borrar el fichero local antiguo
                producto.imagen_url = f"/static/uploads/modelos/{filename}"
        
        db.session.commit()

        flash('Producto terminado actualizado correctamente', 'success')
        return redirect(url_for('productos_bp.index'))

    # Cargar datos en GET (SIN stock físico, SIN modelo, SIN talla)
    if request.method == 'GET':
        form.explosion.data = producto.uuid_explosion
        form.stock_minimo_alerta.data = producto.stock_minimo_alerta
        form.active.data = 1 if producto.active else 0

    return render_template(
        'produccion/productos_terminados/update_producto.html',
        form=form,
        producto=producto,
        explosiones_data=data_explosiones
    )

@productos_bp.route('/eliminar/<uuid>', methods=['POST'])
@login_required
@roles_accepted('admin', 'produccion')
def eliminar_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    
    if producto.stock_fisico_actual > 0:
        flash('No se puede desactivar un producto con stock físico mayor a 0', 'error')
        return redirect(url_for('productos_bp.index'))

    producto.active = False
    db.session.commit()

    flash('Producto terminado desactivado correctamente', 'success')
    return redirect(url_for('productos_bp.index'))


@productos_bp.route('/detalle/<uuid>')
@login_required
@roles_accepted('admin', 'produccion')
def detalle_producto(uuid):
    producto = ProductoTerminado.query.get_or_404(uuid)
    explosion = producto.explosion
    
    return render_template('produccion/productos_terminados/detalle_producto.html', producto=producto, explosion=explosion)
