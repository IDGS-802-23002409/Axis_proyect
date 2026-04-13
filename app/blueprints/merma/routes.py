from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, roles_accepted, current_user
from app.blueprints.merma import merma_bp
from app.blueprints.merma.form import MermaForm
from app.models.mermas import Merma, TipoMermaEnum, ProcesoMermaEnum, TipoEventoMermaEnum, MotivoMermaEnum
from app.models.produccion import OrdenProduccion, EjecucionCorte, EjecucionCorteRollo
from app.models.insumos import Insumo
from app.models.inventario import RolloInventario
from app.models.modelos_productos import ProductoTerminado
from app.utils.database_connection import db
from decimal import Decimal

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
    
    # Mapeo de estado de orden a proceso de merma
    mapeo_procesos = {
        'Pendiente': 'ALMACEN',
        'En Corte': 'CORTE',
        'Confección': 'CONFECCION',
        'Terminado': 'ACABADO'
    }
    proceso_sugerido = mapeo_procesos.get(orden.estado, 'CORTE')
    
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
                    'teorico': float(d.consumo_teorico_unitario) * orden.cantidad_a_producir,
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
                    'nombre': rollo.insumo.nombre,
                    'tipo': 'ROLLO',
                    'usado': float(ecr.metros_usados),
                    'uuid_rollo': rollo.uuid_rollo
                })

    if request.method == 'POST':
        # Nota: El form original de MermaForm es individual, 
        # pero la plantilla create.html usa listas (insumo[], cantidad[]).
        # Procesamos manualmente las listas enviadas por el formulario.
        
        tipo_merma_gral = request.form.get('tipo_merma')
        proceso = request.form.get('proceso')
        tipo_evento = request.form.get('tipo_evento')
        motivo = request.form.get('motivo')
        observaciones = request.form.get('observaciones')
        
        insumos_ids = request.form.getlist('insumo[]')
        rollos_ids = request.form.getlist('rollo[]')
        cantidades = request.form.getlist('cantidad[]')
        
        exito = False
        try:
            for i in range(len(insumos_ids)):
                qty = Decimal(cantidades[i] or 0)
                if qty <= 0:
                    continue
                
                uuid_insumo = insumos_ids[i]
                uuid_rollo = rollos_ids[i] if i < len(rollos_ids) and rollos_ids[i] else None
                
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
                
                # Descontamos de la OP, ya que esas prendas jamás llegarán a terminarse
                if orden.cantidad_a_producir >= qty_prod_dec:
                    orden.cantidad_a_producir -= int(qty_prod_dec)
                else:
                    orden.cantidad_a_producir = 0

                exito = True
                
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
        insumos=insumos_data,
        proceso_sugerido=proceso_sugerido
    )

@merma_bp.route('/crear_manual', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def crear_manual():
    form = MermaForm()
    
    insumos = Insumo.query.filter_by(unidad_medida='PIEZA').all()
    form.uuid_insumo.choices = [('', 'Seleccione un Insumo...')] + [(i.uuid_insumo, i.nombre) for i in insumos]
    
    rollos = RolloInventario.query.filter(RolloInventario.metraje_continuo_actual > 0).all()
    form.uuid_rollo.choices = [('', 'Seleccione un Rollo...')] + [(r.uuid_rollo, f"{r.insumo.nombre if r.insumo else ''} (Rollo {r.uuid_rollo[:6]}) - {r.metraje_continuo_actual}m") for r in rollos]
    
    productos = ProductoTerminado.query.filter_by(active=True).all()
    form.uuid_producto.choices = [('', 'Seleccione un Producto...')] + [(p.uuid_producto, f"{p.sku_especifico} - {p.explosion.nombre_receta if p.explosion else 'Sin Receta'}") for p in productos]

    if form.validate_on_submit():
        tipo_merma = form.tipo_merma.data
        cantidad = Decimal(form.cantidad.data or 0)
        
        exito = False
        nueva_merma = Merma(
            tipo_merma=tipo_merma,
            proceso=form.proceso.data,
            tipo_evento=form.tipo_evento.data,
            motivo=form.motivo.data,
            cantidad=cantidad,
            observaciones=form.observaciones.data,
            es_total=form.es_total.data,
            usuario_creacion=current_user.id,
            usuario_responsable=current_user.id
        )

        try:
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
                
            elif tipo_merma == 'INSUMO':
                uuid_insumo = request.form.get('uuid_insumo')
                if not uuid_insumo:
                    raise Exception('Debe seleccionar un insumo.')
                insumo = Insumo.query.get(uuid_insumo)
                if not insumo or Decimal(str(insumo.stock_total_acumulado or 0)) < cantidad:
                    raise Exception('Stock insuficiente del insumo.')
                insumo.stock_total_acumulado = Decimal(str(insumo.stock_total_acumulado)) - cantidad
                nueva_merma.uuid_insumo = uuid_insumo
                exito = True

            elif tipo_merma == 'PRODUCTO':
                uuid_producto = request.form.get('uuid_producto')
                if not uuid_producto:
                    raise Exception('Debe seleccionar un producto terminado.')
                producto = ProductoTerminado.query.get(uuid_producto)
                if not producto or Decimal(str(producto.stock_fisico_actual or 0)) < cantidad:
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
    merma = db.session.query(Merma).options(
        db.joinedload(Merma.orden_produccion),
        db.joinedload(Merma.insumo),
        db.joinedload(Merma.rollo).joinedload(RolloInventario.insumo),
        db.joinedload(Merma.producto).joinedload(ProductoTerminado.explosion)
    ).get_or_404(uuid_merma)
    
    return render_template('produccion/merma/ver.html', merma=merma)

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
