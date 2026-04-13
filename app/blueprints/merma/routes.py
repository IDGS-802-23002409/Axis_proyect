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
    mermas = Merma.query.order_by(Merma.fecha_creacion.desc()).all()
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
