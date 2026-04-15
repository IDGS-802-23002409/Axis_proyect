from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, roles_accepted, current_user
from app.blueprints.merma import merma_bp
from app.blueprints.merma.form import MermaForm
from app.models.mermas import Merma, TipoMermaEnum, ProcesoMermaEnum, TipoEventoMermaEnum, MotivoMermaEnum
from app.models.produccion import OrdenProduccion, EjecucionCorte, EjecucionCorteRollo
from app.models.insumos import Insumo
from app.models.inventario import RolloInventario
from app.models.modelos_productos import ProductoTerminado
from app.models.usuarios import Usuario
from app.utils.database_connection import db
from decimal import Decimal
from sqlalchemy import func

@merma_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():
    mermas = db.session.query(Merma).options(
        db.joinedload(Merma.orden_produccion),
        db.joinedload(Merma.insumo),
        db.joinedload(Merma.rollo).joinedload(RolloInventario.insumo),
        db.joinedload(Merma.producto).joinedload(ProductoTerminado.explosion)
    ).order_by(Merma.fecha_creacion.desc()).all()
    
    return render_template('produccion/merma/index.html', mermas=mermas)

@merma_bp.route('/registrar/<uuid_op>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def registrar_merma_op(uuid_op):
    orden = OrdenProduccion.query.get_or_404(uuid_op)
    form = MermaForm()
    
    # Obtener cantidad original del corte para cálculos teóricos precisos
    ejecucion_base = EjecucionCorte.query.filter_by(uuid_op=uuid_op).first()
    cantidad_original = Decimal(ejecucion_base.prendas_reales_logradas if ejecucion_base else orden.cantidad_a_producir)
    
    # Obtener insumos relacionados (Receta + Rollos usados si está en corte)
    insumos_data = []
    
    # 1. Insumos de la receta (PIEZAS)
    if orden.producto and orden.producto.explosion:
        for d in orden.producto.explosion.detalles:
            if d.insumo.unidad_medida == 'PIEZA':
                insumos_data.append({
                    'uuid_insumo': d.insumo.uuid_insumo,
                    'nombre': d.insumo.nombre,
                    'tipo': 'INSUMO',
                    'teorico': float(d.consumo_teorico_unitario) * float(cantidad_original),
                    'uuid_rollo': None
                })
    
    # 2. Rollos usados (TELA)
    cortes = EjecucionCorte.query.filter_by(uuid_op=uuid_op).all()
    for c in cortes:
        ec_rollos = EjecucionCorteRollo.query.filter_by(uuid_corte=c.uuid_corte).all()
        for ecr in ec_rollos:
            rollo = RolloInventario.query.get(ecr.uuid_rollo)
            if rollo:
                insumos_data.append({
                    'uuid_insumo': rollo.uuid_insumo,
                    'nombre': rollo.insumo.nombre if rollo.insumo else "Sin Nombre de Insumo",
                    'tipo': 'ROLLO',
                    'usado': float(ecr.metros_usados),
                    'uuid_rollo': rollo.uuid_rollo
                })

    if request.method == 'POST':
        tipo_merma_gral = request.form.get('tipo_merma')
        proceso = 'ALMACEN'
        tipo_evento = request.form.get('tipo_evento')
        motivo = request.form.get('motivo')
        observaciones = request.form.get('observaciones')
        
        insumos_ids = request.form.getlist('insumo[]')
        rollos_ids = request.form.getlist('rollo[]')
        cantidades = request.form.getlist('cantidad[]')
        
        # Mapeo de insumo -> consumo unitario para recálculo de capacidad
        consumos_receta = {}
        if orden.producto and orden.producto.explosion:
            for d in orden.producto.explosion.detalles:
                consumos_receta[d.uuid_insumo] = Decimal(str(d.consumo_teorico_unitario))

        # Diccionario para validación rápida en servidor
        limites = {}
        for item in insumos_data:
            key = (item['uuid_insumo'], item['uuid_rollo'])
            limites[key] = Decimal(item.get('usado') or item.get('teorico') or 0)

        exito = False
        try:
            cantidad_previa_op = orden.cantidad_a_producir
            
            for i in range(len(insumos_ids)):
                qty = Decimal(cantidades[i] or 0)
                if qty <= 0:
                    continue
                
                uuid_insumo = insumos_ids[i]
                uuid_rollo = rollos_ids[i] if i < len(rollos_ids) and rollos_ids[i] else None
                
                # VALIDACIÓN SERVIDOR
                max_permitido = limites.get((uuid_insumo, uuid_rollo), Decimal(0))
                if qty > (max_permitido + Decimal('0.0001')):
                    raise Exception(f"La cantidad de merma ({qty}) excede el límite permitido ({max_permitido}) para el insumo.")

                # Crear registro de merma
                nueva_merma = Merma(
                    tipo_merma='TELA' if uuid_rollo else 'INSUMO',
                    proceso=proceso,
                    tipo_evento=tipo_evento,
                    motivo=motivo,
                    uuid_op=uuid_op,
                    uuid_insumo=uuid_insumo,
                    uuid_rollo=uuid_rollo,
                    cantidad=qty,
                    observaciones=observaciones,
                    usuario_creacion=current_user.id,
                    usuario_responsable=current_user.id
                )
                db.session.add(nueva_merma)
                
                # RECALCULAR CAPACIDAD DE LA OP
                # Usamos la cantidad_original para evitar errores acumulativos
                consumo_u = consumos_receta.get(uuid_insumo)
                if consumo_u and consumo_u > 0:
                    # Buscamos todas las mermas activas para este insumo en esta OP (incluyendo la actual)
                    # Para simplificar, usaremos el total acumulado en esta transacción
                    
                    # 1. Mermas previas
                    total_merma_insumo = db.session.query(func.sum(Merma.cantidad)).filter(
                        Merma.uuid_op == uuid_op,
                        Merma.uuid_insumo == uuid_insumo,
                        Merma.activo == True
                    ).scalar() or Decimal(0)
                    
                    # 2. Sumar la actual (que aún no está commit pero ya está en el session)
                    total_merma_insumo += qty
                    
                    cantidad_disponible = (consumo_u * cantidad_original) - total_merma_insumo
                    posibles = int(cantidad_disponible // consumo_u)
                    
                    if posibles < orden.cantidad_a_producir:
                        orden.cantidad_a_producir = posibles

                # Descuento de Inventario
                if uuid_rollo:
                    rollo = RolloInventario.query.get(uuid_rollo)
                    if rollo:
                        rollo.metraje_continuo_actual -= qty
                        # También descontar del acumulado del insumo
                        insumo = Insumo.query.get(uuid_insumo)
                        if insumo:
                            insumo.stock_total_acumulado -= qty
                else:
                    insumo = Insumo.query.get(uuid_insumo)
                    if insumo:
                        insumo.stock_total_acumulado -= qty
                
                exito = True

            # Procesar merma de prenda completa (PRODUCTO)
            qty_producto = request.form.get('cantidad_producto', type=int)
            if qty_producto and qty_producto > 0:
                qty_prod_dec = Decimal(qty_producto)
                nueva_merma_prod = Merma(
                    tipo_merma='PRODUCTO',
                    proceso=proceso,
                    tipo_evento=tipo_evento,
                    motivo=motivo,
                    uuid_op=uuid_op,
                    uuid_producto=orden.uuid_producto,
                    cantidad=qty_prod_dec,
                    observaciones=observaciones,
                    usuario_creacion=current_user.id,
                    usuario_responsable=current_user.id
                )
                db.session.add(nueva_merma_prod)
                
                if orden.cantidad_a_producir >= qty_prod_dec:
                    orden.cantidad_a_producir -= int(qty_prod_dec)
                else:
                    orden.cantidad_a_producir = 0

                exito = True

            # LANZAR NUEVA ORDEN PARA FALTANTES SI ES VENTA
            if exito and (orden.uuid_pedido_detalle or orden.uuid_venta_detalle):
                diferencia = cantidad_previa_op - orden.cantidad_a_producir
                if diferencia > 0:
                    nueva_op = OrdenProduccion(
                        uuid_producto=orden.uuid_producto,
                        uuid_venta=orden.uuid_venta,
                        uuid_venta_detalle=orden.uuid_venta_detalle,
                        uuid_pedido_detalle=orden.uuid_pedido_detalle,
                        cantidad_a_producir=int(diferencia),
                        estado='Pendiente'
                    )
                    db.session.add(nueva_op)
                    flash(f'Se ha generado una nueva orden por {int(diferencia)} prendas faltantes para cumplir con el pedido.', 'info')
                
            if exito:
                db.session.commit()
                flash('Merma registrada y stock actualizado correctamente', 'success')
            else:
                flash('No se ingresaron cantidades de merma válidas', 'warning')
                
            return redirect(url_for('orden_bp.ver', uuid_op=uuid_op))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar merma: {str(e)}', 'error')

    return render_template(
        'produccion/merma/create.html', 
        form=form, 
        orden=orden, 
        insumos=insumos_data
    )

@merma_bp.route('/crear_manual', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def crear_manual():
    form = MermaForm()
    
    #  Traer TODOS los insumos (no solo PIEZA)
    insumos = Insumo.query.all()
    form.uuid_insumo.choices = [('', 'Seleccione un Insumo...')] + [
        (i.uuid_insumo, f"{i.nombre} ({i.unidad_medida})") for i in insumos
    ]
    
    rollos = RolloInventario.query.filter(RolloInventario.metraje_continuo_actual > 0).all()
    form.uuid_rollo.choices = [('', 'Seleccione un Rollo...')] + [
        (r.uuid_rollo, f"{r.insumo.nombre if r.insumo else ''} (Rollo {r.uuid_rollo[:6]}) - {r.metraje_continuo_actual}m")
        for r in rollos
    ]
    
    productos = ProductoTerminado.query.filter_by(active=True).all()
    form.uuid_producto.choices = [('', 'Seleccione un Producto...')] + [
        (p.uuid_producto, f"{p.sku_especifico} - {p.explosion.nombre_receta if p.explosion else 'Sin Receta'}")
        for p in productos
    ]

    if form.validate_on_submit():
        tipo_merma = form.tipo_merma.data
        cantidad = Decimal(form.cantidad.data or 0)

        #  VALIDACIÓN GLOBAL
        if cantidad <= 0:
            flash('La cantidad debe ser mayor a 0.', 'danger')
            return redirect(request.url)
        
        exito = False
        nueva_merma = Merma(
            tipo_merma=tipo_merma,
            proceso='ALMACEN',
            tipo_evento=form.tipo_evento.data,
            motivo=form.motivo.data,
            cantidad=cantidad,
            observaciones=form.observaciones.data,
            es_total=form.es_total.data,
            usuario_creacion=current_user.id,
            usuario_responsable=current_user.id
        )

        try:
            # ─────────────────────────────
            # TELA (permite decimales)
            # ─────────────────────────────
            if tipo_merma == 'TELA':
                uuid_rollo = request.form.get('uuid_rollo')
                if not uuid_rollo:
                    raise Exception('Debe seleccionar un rollo de tela.')

                rollo = RolloInventario.query.get(uuid_rollo)

                if not rollo or Decimal(str(rollo.metraje_continuo_actual or 0)) < cantidad:
                    raise Exception('Metraje insuficiente o rollo no encontrado.')

                rollo.metraje_continuo_actual = Decimal(str(rollo.metraje_continuo_actual)) - cantidad

                if rollo.insumo:
                    rollo.insumo.stock_total_acumulado = Decimal(str(rollo.insumo.stock_total_acumulado or 0)) - cantidad

                nueva_merma.uuid_rollo = uuid_rollo
                nueva_merma.uuid_insumo = rollo.uuid_insumo
                exito = True

            # ─────────────────────────────
            # INSUMO (validar PIEZA vs DECIMAL)
            # ─────────────────────────────
            elif tipo_merma == 'INSUMO':
                uuid_insumo = request.form.get('uuid_insumo')
                if not uuid_insumo:
                    raise Exception('Debe seleccionar un insumo.')

                insumo = Insumo.query.get(uuid_insumo)
                if not insumo:
                    raise Exception('Insumo no encontrado.')

                #  VALIDACIÓN CLAVE
                if insumo.unidad_medida == 'PIEZA':
                    if cantidad % 1 != 0:
                        raise Exception('Las piezas deben ser números enteros.')

                if Decimal(str(insumo.stock_total_acumulado or 0)) < cantidad:
                    raise Exception('Stock insuficiente del insumo.')

                insumo.stock_total_acumulado = Decimal(str(insumo.stock_total_acumulado)) - cantidad

                nueva_merma.uuid_insumo = uuid_insumo
                exito = True

            # ─────────────────────────────
            # PRODUCTO (siempre entero)
            # ─────────────────────────────
            elif tipo_merma == 'PRODUCTO':
                uuid_producto = request.form.get('uuid_producto')
                if not uuid_producto:
                    raise Exception('Debe seleccionar un producto terminado.')

                producto = ProductoTerminado.query.get(uuid_producto)
                if not producto:
                    raise Exception('Producto no encontrado.')

                #  VALIDACIÓN: productos siempre enteros
                if cantidad % 1 != 0:
                    raise Exception('Los productos deben ser cantidades enteras.')

                if Decimal(str(producto.stock_fisico_actual or 0)) < cantidad:
                    raise Exception('Stock físico insuficiente del producto terminado.')

                producto.stock_fisico_actual = int(producto.stock_fisico_actual or 0) - int(cantidad)

                nueva_merma.uuid_producto = uuid_producto
                exito = True

            if exito:
                db.session.add(nueva_merma)
                db.session.commit()
                flash('Merma manual registrada correctamente.', 'success')
                return redirect(url_for('merma_bp.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar merma: {str(e)}', 'danger')

    return render_template('produccion/merma/create_manual.html', form=form)

@merma_bp.route('/ver/<uuid_merma>')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def ver(uuid_merma):

    # Traer la merma con relaciones
    merma = db.session.query(Merma).options(
        db.joinedload(Merma.orden_produccion),
        db.joinedload(Merma.insumo),
        db.joinedload(Merma.rollo).joinedload(RolloInventario.insumo),
        db.joinedload(Merma.producto).joinedload(ProductoTerminado.explosion)
    ).get_or_404(uuid_merma)

    # ─────────────────────────────
    # BUSCAR USUARIO POR UUID
    # ─────────────────────────────
    nombre_usuario = None

    if merma.usuario_creacion:
        usuario = db.session.query(Usuario).filter(
            Usuario.id == merma.usuario_creacion
        ).first()

        if usuario:
            nombre_usuario = usuario.nombre_completo

    return render_template(
        'produccion/merma/ver.html',
        merma=merma,
        nombre_usuario=nombre_usuario
    )

@merma_bp.route('/anular/<uuid_merma>', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def anular(uuid_merma):
    merma = Merma.query.get_or_404(uuid_merma)
    
    if not merma.activo:
        flash('La merma ya está anulada', 'warning')
        return redirect(url_for('merma_bp.ver', uuid_merma=uuid_merma))
        
    try:
        tipo = merma.tipo_merma.name if hasattr(merma.tipo_merma, 'name') else merma.tipo_merma
        if tipo == 'TELA':
            if merma.rollo:
                merma.rollo.metraje_continuo_actual = Decimal(str(merma.rollo.metraje_continuo_actual or 0)) + merma.cantidad
            if merma.insumo:
                merma.insumo.stock_total_acumulado = Decimal(str(merma.insumo.stock_total_acumulado or 0)) + merma.cantidad
        elif tipo == 'INSUMO':
            if merma.insumo:
                merma.insumo.stock_total_acumulado = Decimal(str(merma.insumo.stock_total_acumulado or 0)) + merma.cantidad
        elif tipo == 'PRODUCTO':
            if merma.producto:
                if not merma.uuid_op:
                    merma.producto.stock_fisico_actual = int(merma.producto.stock_fisico_actual or 0) + int(merma.cantidad)
                else: 
                    if merma.orden_produccion and merma.orden_produccion.estado != 'Terminado':
                        merma.orden_produccion.cantidad_a_producir += int(merma.cantidad)
                    
        merma.activo = False
        merma.usuario_actualizacion = current_user.id
        db.session.commit()
        flash('Merma anulada y stock retornado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al anular la merma: {str(e)}', 'danger')

    return redirect(url_for('merma_bp.ver', uuid_merma=uuid_merma))
