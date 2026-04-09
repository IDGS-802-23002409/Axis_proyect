from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_security import login_required, roles_required, roles_accepted, current_user

from app.blueprints.merma import merma_bp
from app.blueprints.merma.form import MermaForm, RetazoForm
from app.models.produccion import MermaPiezas, OrdenProduccion, EjecucionCorte
from app.models.explosion_materiales import ExplosionMaterialesDetalle, ExplosionMaterialesCabecera
from app.models.insumos import Insumo
from app.models.inventario import RolloInventario, RetazoInventario
from app.models.usuarios import Usuario
from app.utils.database_connection import db
import logging

logger = logging.getLogger(__name__)

def _registrar_retazo_defecto(uuid_corte: str, metraje: float) -> None:
    ejecucion = EjecucionCorte.query.get(uuid_corte)
    if not ejecucion:
        return
    ejecucion.merma_real_calculada = (
        float(ejecucion.merma_real_calculada) + metraje
    )

@merma_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente')
def index():
    op_uuid     = request.args.get('op', '').strip()
    insumo_uuid = request.args.get('insumo', '').strip()
    motivo      = request.args.get('motivo', '').strip()

    q = MermaPiezas.query

    if op_uuid:
        q = q.filter(MermaPiezas.uuid_op == op_uuid)
    if insumo_uuid:
        q = q.filter(MermaPiezas.uuid_insumo == insumo_uuid)
    if motivo:
        q = q.filter(MermaPiezas.motivo == motivo)

    mermas = q.order_by(MermaPiezas.fecha_registro.desc()).all()

    merma_total = sum(
        float(m.cantidad_real_consumida) - float(m.cantidad_teorica)
        for m in mermas
        if (float(m.cantidad_real_consumida) - float(m.cantidad_teorica)) > 0
    )
    ahorro_total = abs(sum(
        float(m.cantidad_real_consumida) - float(m.cantidad_teorica)
        for m in mermas
        if (float(m.cantidad_real_consumida) - float(m.cantidad_teorica)) < 0
    ))

    ordenes = OrdenProduccion.query.order_by(OrdenProduccion.fecha_solicitud.desc()).all()
    insumos = (
        Insumo.query
        .filter_by(estatus='ACTIVO', contenido_unidad_medida='PIEZA')
        .order_by(Insumo.nombre)
        .all()
    )

    return render_template(
        'produccion/merma/index.html',
        mermas=mermas,
        total_mermas=len(mermas),
        merma_total=merma_total,
        ahorro_total=ahorro_total,
        ordenes=ordenes,
        insumos=insumos,
        filtro_op=op_uuid,
        filtro_insumo=insumo_uuid,
        filtro_motivo=motivo,
    )

@merma_bp.route('/insumos-por-op/<uuid_op>')
@login_required
@roles_accepted('admin', 'gerente')
def insumos_por_op(uuid_op):
    """
    AJAX — devuelve los insumos PIEZA de la explosión de materiales
    del producto asociado a la OP seleccionada, junto con la cantidad
    teórica sugerida (consumo_teorico_unitario × cantidad_a_producir).
    """
    op = OrdenProduccion.query.get_or_404(uuid_op)

    if not op.producto or not op.producto.explosion:
        return jsonify({'insumos': [], 'error': 'Esta OP no tiene explosión de materiales definida.'})

    detalles = (
        ExplosionMaterialesDetalle.query
        .filter_by(uuid_explosion=op.producto.explosion.uuid_explosion)
        .join(Insumo, ExplosionMaterialesDetalle.uuid_insumo == Insumo.uuid_insumo)
        .filter(
            Insumo.contenido_unidad_medida == 'PIEZA',
            Insumo.estatus == 'ACTIVO'
        )
        .all()
    )

    if not detalles:
        return jsonify({'insumos': [], 'error': 'No hay insumos tipo PIEZA en la explosión de esta OP.'})

    return jsonify({
        'insumos': [
            {
                'uuid':                    d.uuid_insumo,
                'nombre':                  d.insumo.nombre,
                'sku':                     d.insumo.sku,
                'stock_actual':            float(d.insumo.stock_total_acumulado),
                'consumo_unitario':        float(d.consumo_teorico_unitario),
                'cantidad_op':             op.cantidad_a_producir,
                'cantidad_teorica_sugerida': round(
                    float(d.consumo_teorico_unitario) * op.cantidad_a_producir
                ),
            }
            for d in detalles
        ],
        'error': None
    })


@merma_bp.route('/insumo-por-corte/<uuid_corte>')
@login_required
@roles_accepted('admin', 'gerente')
def insumo_por_corte(uuid_corte):
    """
    devuelve el insumo (tela) que se usó en una ejecución de corte,
    basado en el producto asociado a su OP.
    """
    ejecucion = EjecucionCorte.query.get_or_404(uuid_corte)
    
    if not ejecucion.orden_produccion or not ejecucion.orden_produccion.producto:
        return jsonify({'insumo': None, 'error': 'No se encontró producto para este corte'})
    
    # El insumo de un corte es el TELA (METRO) del producto de la OP
    producto = ejecucion.orden_produccion.producto
    if not producto.explosion:
        return jsonify({'insumo': None, 'error': 'El producto no tiene explosión de materiales'})
    
    insumo_tela = (
        ExplosionMaterialesDetalle.query
        .filter_by(uuid_explosion=producto.explosion.uuid_explosion)
        .join(Insumo)
        .filter(Insumo.contenido_unidad_medida == 'METRO')
        .first()
    )
    
    if not insumo_tela:
        return jsonify({'insumo': None, 'error': 'No se encontró insumo TELA para este producto'})
    
    return jsonify({
        'insumo': {
            'uuid_insumo': insumo_tela.uuid_insumo,
            'nombre': insumo_tela.insumo.nombre,
            'sku': insumo_tela.insumo.sku,
            'stock_actual': float(insumo_tela.insumo.stock_total_acumulado),
        },
        'error': None
    })


@merma_bp.route('/rollos-por-corte/<uuid_corte>')
@login_required
@roles_accepted('admin', 'gerente')
def rollos_por_corte(uuid_corte):
    """
    devuelve los rollos disponibles que coincidan con el insumo (TELA)
    del producto de la OP asociada al corte seleccionado.
    """
    ejecucion = EjecucionCorte.query.get_or_404(uuid_corte)
    
    if not ejecucion.orden_produccion or not ejecucion.orden_produccion.producto:
        return jsonify({'rollos': [], 'error': 'No se encontró producto para este corte'})
    
    producto = ejecucion.orden_produccion.producto
    if not producto.explosion:
        return jsonify({'rollos': [], 'error': 'El producto no tiene explosión de materiales'})
    
    insumo_tela = (
        ExplosionMaterialesDetalle.query
        .filter_by(uuid_explosion=producto.explosion.uuid_explosion)
        .join(Insumo)
        .filter(Insumo.contenido_unidad_medida == 'METRO')
        .first()
    )
    
    if not insumo_tela:
        return jsonify({'rollos': [], 'error': 'No se encontró insumo TELA para este producto'})
    
    # Obtener rollos del insumo TELA con metraje disponible
    rollos = (
        RolloInventario.query
        .filter_by(uuid_insumo=insumo_tela.uuid_insumo)
        .filter(RolloInventario.metraje_continuo_actual > 0)
        .order_by(RolloInventario.fecha_creacion.desc())
        .all()
    )
    
    return jsonify({
        'rollos': [
            {
                'uuid_rollo': r.uuid_rollo,
                'nombre': f"{r.insumo.nombre if r.insumo else 'N/A'}",
                'metraje_disponible': float(r.metraje_continuo_actual),
                'display': f"{r.insumo.nombre if r.insumo else 'N/A'} · {float(r.metraje_continuo_actual):.2f} m disponibles"
            }
            for r in rollos
        ],
        'error': None
    })


@merma_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente')
def registro_merma():
    form = MermaForm()

    if form.validate_on_submit():
        try:
            merma = MermaPiezas(
                uuid_op=form.orden_produccion.data,
                uuid_insumo=form.insumo.data,
                cantidad_teorica=form.cantidad_teorica.data,
                cantidad_real_consumida=form.cantidad_real_consumida.data,
                motivo=form.motivo.data or None,
                observaciones=form.observaciones.data or None,
                usuario_registro_uuid=current_user.uuid_usuario,
            )
            db.session.add(merma)

            diferencia = int(form.cantidad_real_consumida.data) - int(form.cantidad_teorica.data)
            if diferencia > 0:
                insumo = Insumo.query.get(form.insumo.data)
                stock_antes = float(insumo.stock_total_acumulado)
                insumo.stock_total_acumulado = stock_antes - diferencia
                db.session.add(insumo)

                logger.info(
                    f"[MERMA-STOCK] OP={form.orden_produccion.data} | "
                    f"Insumo={insumo.nombre} ({insumo.uuid_insumo}) | "
                    f"Stock antes={stock_antes} | "
                    f"Descuento={diferencia} pzas | "
                    f"Stock después={float(insumo.stock_total_acumulado)} | "
                    f"Usuario={current_user.email}"
                )

            db.session.commit()
            flash('Merma registrada correctamente.', 'success')
            return redirect(url_for('merma.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar merma: {str(e)}', 'error')

    return render_template('produccion/merma/registro_merma.html', form=form)


@merma_bp.route('/detalle/<uuid_merma>')
@login_required
@roles_accepted('admin', 'gerente')
def detalle_merma(uuid_merma):
    merma = MermaPiezas.query.get_or_404(uuid_merma)

    usuario_registro = None
    if merma.usuario_registro_uuid:
        usuario_registro = Usuario.query.filter_by(
            uuid_usuario=merma.usuario_registro_uuid
        ).first()

    return render_template(
        'produccion/merma/detalle_merma.html',
        merma=merma,
        usuario_registro=usuario_registro,
        diferencia=int(merma.cantidad_real_consumida) - int(merma.cantidad_teorica),
    )


@merma_bp.route('/eliminar/<uuid_merma>', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def eliminar_merma(uuid_merma):
    merma = MermaPiezas.query.get_or_404(uuid_merma)

    if merma.orden_produccion and merma.orden_produccion.estado == 'Terminado':
        flash(
            'No se puede eliminar una merma de una orden ya terminada. '
            'Contacta al administrador si hubo un error.',
            'error'
        )
        return redirect(url_for('merma.detalle_merma', uuid_merma=uuid_merma))

    try:
        diferencia = int(merma.cantidad_real_consumida) - int(merma.cantidad_teorica)
        if diferencia > 0:
            insumo = Insumo.query.get(merma.uuid_insumo)
            if insumo:
                stock_antes = float(insumo.stock_total_acumulado)
                insumo.stock_total_acumulado = stock_antes + diferencia
                db.session.add(insumo)

                logger.info(
                    f"[MERMA-REVERT] Merma={uuid_merma} | "
                    f"Insumo={insumo.nombre} ({insumo.uuid_insumo}) | "
                    f"Stock antes={stock_antes} | "
                    f"Revertido={diferencia} pzas | "
                    f"Stock después={float(insumo.stock_total_acumulado)} | "
                    f"Usuario={current_user.email}"
                )

        db.session.delete(merma)
        db.session.commit()
        flash('Merma eliminada.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')

    return redirect(url_for('merma.index'))

@merma_bp.route('/retazos')
@login_required
@roles_accepted('admin', 'gerente')
def index_retazos():
    retazos = (
        RetazoInventario.query
        .order_by(RetazoInventario.fecha_creacion.desc())
        .all()
    )
    
    metraje_total = sum(float(r.metraje) for r in retazos)
    defectos_count = sum(1 for r in retazos if r.motivo_merma and r.motivo_merma.strip())
    
    return render_template('produccion/merma/index_retazos.html', retazos=retazos, metraje_total=metraje_total, defectos_count=defectos_count)


@merma_bp.route('/retazos/registro', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente')
def registro_retazo():
    form = RetazoForm()

    if form.validate_on_submit():
        try:
            metraje = float(form.metraje.data)
            
            # Validaciones
            ejecucion = EjecucionCorte.query.get(form.ejecucion_corte.data)
            if not ejecucion:
                flash('La ejecución de corte no existe.', 'error')
                return redirect(url_for('merma.registro_retazo'))
            
            rollo = RolloInventario.query.get(form.rollo_origen.data)
            if not rollo:
                flash('El rollo no existe.', 'error')
                return redirect(url_for('merma.registro_retazo'))
            
            # Verificar que el rollo tiene suficiente metraje
            if float(rollo.metraje_continuo_actual) < metraje:
                flash(f'El rollo no tiene suficiente metraje. Disponible: {float(rollo.metraje_continuo_actual):.2f}m, Solicitado: {metraje:.2f}m', 'error')
                return redirect(url_for('merma.registro_retazo'))
            
            # Verificar coincidencia de insumo TELA del corte
            if not ejecucion.orden_produccion or not ejecucion.orden_produccion.producto:
                flash('La orden de producción no tiene producto asociado.', 'error')
                return redirect(url_for('merma.registro_retazo'))
            
            producto = ejecucion.orden_produccion.producto
            if not producto.explosion:
                flash('El producto no tiene explosión de materiales.', 'error')
                return redirect(url_for('merma.registro_retazo'))
            
            insumo_tela_esperado = (
                ExplosionMaterialesDetalle.query
                .filter_by(uuid_explosion=producto.explosion.uuid_explosion)
                .join(Insumo)
                .filter(Insumo.contenido_unidad_medida == 'METRO')
                .first()
            )
            
            if not insumo_tela_esperado:
                flash('No se encontró insumo TELA para este producto.', 'error')
                return redirect(url_for('merma.registro_retazo'))
            
            if rollo.uuid_insumo != insumo_tela_esperado.uuid_insumo:
                flash(
                    f'El rollo ({rollo.insumo.nombre}) no pertenece al insumo TELA del corte ({insumo_tela_esperado.insumo.nombre}).',
                    'error'
                )
                return redirect(url_for('merma.registro_retazo'))

            # Crear retazo
            retazo = RetazoInventario(
                uuid_rollo_origen=form.rollo_origen.data,
                uuid_corte_origen=form.ejecucion_corte.data,
                metraje=metraje,
                motivo_merma=form.motivo_merma.data or None,
            )
            db.session.add(retazo)

            stock_rollo_antes = float(rollo.metraje_continuo_actual)
            stock_insumo_antes = float(rollo.insumo.stock_total_acumulado)

            rollo.metraje_continuo_actual = stock_rollo_antes - metraje
            rollo.insumo.stock_total_acumulado = stock_insumo_antes - metraje
            db.session.add(rollo)
            db.session.add(rollo.insumo)

            # Si hay motivo_merma, es un defecto que afecta la merma de la OP
            if form.motivo_merma.data:
                _registrar_retazo_defecto(form.ejecucion_corte.data, metraje)

            logger.info(
                f"[RETAZO-STOCK] EsDefecto={bool(form.motivo_merma.data)} | "
                f"Corte={ejecucion.uuid_corte[:8]} | "
                f"Rollo={rollo.uuid_rollo[:8]} | "
                f"Insumo={rollo.insumo.nombre} | "
                f"Rollo antes={stock_rollo_antes:.2f}m → después={float(rollo.metraje_continuo_actual):.2f}m | "
                f"Stock insumo antes={stock_insumo_antes:.2f}m → después={float(rollo.insumo.stock_total_acumulado):.2f}m | "
                f"Usuario={current_user.email}"
            )

            db.session.commit()
            flash('Retazo registrado correctamente.', 'success')
            return redirect(url_for('merma.index_retazos'))

        except Exception as e:
            db.session.rollback()
            logger.error(f"[RETAZO-ERROR] {str(e)}", exc_info=True)
            flash(f'Error al registrar retazo: {str(e)}', 'error')

    return render_template('produccion/merma/registro_retazo.html', form=form)



@merma_bp.route('/retazos/detalle/<uuid_retazo>')
@login_required
@roles_accepted('admin', 'gerente')
def detalle_retazo(uuid_retazo):
    retazo = RetazoInventario.query.get_or_404(uuid_retazo)
    return render_template('produccion/merma/detalle_retazo.html', retazo=retazo)


@merma_bp.route('/retazos/eliminar/<uuid_retazo>', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def eliminar_retazo(uuid_retazo):
    retazo = RetazoInventario.query.get_or_404(uuid_retazo)

    ejecucion = EjecucionCorte.query.get(retazo.uuid_corte_origen)
    if ejecucion and ejecucion.orden_produccion and \
            ejecucion.orden_produccion.estado == 'Terminado':
        flash('No se puede eliminar un retazo de una orden ya terminada.', 'error')
        return redirect(url_for('merma.detalle_retazo', uuid_retazo=uuid_retazo))

    try:
        metraje = float(retazo.metraje)

        rollo = RolloInventario.query.get(retazo.uuid_rollo_origen)
        if rollo:
            rollo.metraje_continuo_actual = float(rollo.metraje_continuo_actual) + metraje
            rollo.insumo.stock_total_acumulado = float(rollo.insumo.stock_total_acumulado) + metraje
            db.session.add(rollo)
            db.session.add(rollo.insumo)

        if ejecucion:
            ejecucion.merma_real_calculada = max(
                0.0,
                float(ejecucion.merma_real_calculada) - metraje
            )
            db.session.add(ejecucion)

        db.session.delete(retazo)
        db.session.commit()
        flash('Retazo eliminado.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')

    return redirect(url_for('merma.index_retazos'))