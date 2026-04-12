from flask import flash, redirect, render_template, request, url_for
from app.blueprints.orden_produccion import orden_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado

from app.utils.database_connection import db
from flask_security import login_required, roles_accepted
from sqlalchemy.orm import joinedload
from decimal import Decimal
from app.models.explosion_materiales import ExplosionMaterialesDetalle
from app.models.inventario import RolloInventario
from app.models.insumos import Insumo
from app.models.produccion import OrdenProduccion, EjecucionCorte
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.utils.database_connection import db
from .forms import OrdenProduccionForm


@orden_bp.route("/")
@login_required
@roles_accepted("admin", "gerente", "produccion")
def index():

    ordenes = (
        db.session.query(OrdenProduccion)
        .join(ProductoTerminado)
        .order_by(OrdenProduccion.fecha_solicitud.desc())
        .all()
    )

    return render_template("produccion/orden/index.html", ordenes=ordenes)


"""
@orden_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def create():

    form = OrdenProduccionForm()

    # Productos activos
    productos = ProductoTerminado.query.filter_by(active=True).all()
    form.uuid_producto.choices = [
        (p.uuid_producto, f"{p.sku_especifico} - {p.explosion.nombre_receta} ({p.explosion.talla})")
        for p in productos
    ]

    #  Ventas (opcional)
    ventas = VentaDetalle.query.all()
    form.uuid_venta_detalle.choices = [('', 'Sin relación (Producción para stock)')] + [
        (v.uuid_detalle, f"Venta #{v.uuid_detalle}")
        for v in ventas
    ]

    if form.validate_on_submit():

        producto = ProductoTerminado.query.get(form.uuid_producto.data)

        if not producto or not producto.explosion:
            flash("El producto no existe o no tiene receta", "danger")
            return redirect(url_for('orden_bp.index'))

        uuid_venta = form.uuid_venta_detalle.data or None

        #  Determinar cantidad
        cantidad = int(form.cantidad_a_producir.data)
        
        if uuid_venta:
            venta = VentaDetalle.query.get(uuid_venta)
            if not venta:
                flash("La venta seleccionada no existe", "danger")
                return redirect(url_for('orden_bp.index'))
            tipo = 'PEDIDO'
            
            # Validate that produced quantity is at least the sale quantity
            if cantidad < venta.cantidad:
                flash(f"La cantidad a producir ({cantidad}) no cubre la venta ({venta.cantidad}).", "danger")
                return render_template('produccion/orden/create.html', form=form)
        else:
            tipo = 'STOCK'

        # REGLA: Las recetas se manejan por lotes (1 lote = 10 unidades).
        if cantidad % 10 != 0:
            flash(f"La cantidad a producir debe ser en lotes de 10 (ej: 10, 20, 30...). Cantidad ingresada: {cantidad}", "warning")
            return render_template('produccion/orden/create.html', form=form)

        try:
            # Crear orden en estado PENDIENTE
            orden = OrdenProduccion(
                uuid_producto=producto.uuid_producto,
                uuid_venta_detalle=uuid_venta,
                cantidad_a_producir=cantidad,
                estado='Pendiente'
            )
            db.session.add(orden)
            db.session.flush()

            # Reserva de Materiales: Descuenta el inventario desde el inicio
            for detalle in producto.explosion.detalles:
                consumo_unitario = Decimal(detalle.consumo_teorico_unitario)
                
                # Descuento del total general
                cantidad_total_necesaria = consumo_unitario * Decimal(cantidad)
                insumo = Insumo.query.get(detalle.uuid_insumo)
                if insumo.stock_total_acumulado < cantidad_total_necesaria:
                    raise Exception(f"Stock insuficiente general para el insumo {insumo.nombre}. Requerido: {cantidad_total_necesaria}, Disponible: {insumo.stock_total_acumulado}")
                
                insumo.stock_total_acumulado -= cantidad_total_necesaria

                # Si es tela (ROLLO), hacer FIFO en los rollos físicos
                if insumo.unidad_medida == "ROLLO":
                    prendas_restantes = cantidad

                    rollos = RolloInventario.query.filter(
                        RolloInventario.uuid_insumo == detalle.uuid_insumo,
                        RolloInventario.metraje_continuo_actual > 0
                    ).order_by(RolloInventario.fecha_creacion.asc()).all()

                    for rollo in rollos:
                        metraje_disponible = Decimal(rollo.metraje_continuo_actual)
                        prendas_de_este_rollo = int(metraje_disponible // consumo_unitario)

                        if prendas_de_este_rollo <= 0:
                            continue

                        prendas_a_usar = min(prendas_restantes, prendas_de_este_rollo)
                        metros_a_descontar = Decimal(prendas_a_usar) * consumo_unitario

                        rollo.metraje_continuo_actual -= metros_a_descontar

                        if rollo.metraje_continuo_actual <= Decimal('0.0001'):
                            rollo.metraje_continuo_actual = Decimal('0.0000')

                        corte = EjecucionCorte(
                            uuid_op=orden.uuid_op,
                            uuid_rollo_used=rollo.uuid_rollo,
                            metros_teoricos_requeridos=metros_a_descontar,
                            metros_sacados_bodega=metros_a_descontar,
                            prendas_reales_logradas=prendas_a_usar,
                            merma_real_calculada=Decimal('0.0000')
                        )
                        db.session.add(corte)

                        prendas_restantes -= prendas_a_usar

                        if prendas_restantes == 0:
                            break

                    if prendas_restantes > 0:
                        raise Exception(f"No hay suficientes rollos disponibles con metraje continuo para el insumo {insumo.nombre}")

            db.session.commit()

            flash(
                "Orden de producción creada y materiales reservados.",
                "success"
            )
            return redirect(url_for('orden_bp.index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la orden: {str(e)}", "danger")
            return redirect(url_for('orden_bp.index'))

    return render_template('produccion/orden/create.html', form=form)
"""
# CREAR UNA ORDEN DE PRODUCCION QUE NO FUE PEDIDO DE UN CLIENTE, NO TIENE VENTA RELACIONADA
# YA NO SE CREA POR LOTES SE INGRESAN LAS PRENDAS A PRODUCIR
# SE DESCUENTAN INSUMOS Y TELA HASTA QUE SU ESTADO PASA A CORTE, SIMPLEMENTE SE CREA LA  SOLICITUD

@orden_bp.route("/crear", methods=["GET", "POST"])
@login_required
@roles_accepted("admin", "gerente", "produccion")
def create():

    form = OrdenProduccionForm()

    # 🔥 SIEMPRE cargar productos activos
    productos = ProductoTerminado.query.filter_by(active=True).all()

    form.uuid_producto.choices = [
        ("", "Seleccione una prenda")
    ] + [
        (
            str(p.uuid_producto),
            f"{p.sku_especifico} - {p.explosion.nombre_receta} ({p.explosion.talla})",
        )
        for p in productos
    ]

    if form.validate_on_submit():

        if not form.uuid_producto.data:
            flash("Debes seleccionar una prenda", "warning")
            return redirect(url_for("orden_bp.create"))

        producto = ProductoTerminado.query.get(form.uuid_producto.data)

        if not producto:
            flash("El producto no existe", "danger")
            return redirect(url_for("orden_bp.create"))

        try:
            cantidad = int(form.cantidad_a_producir.data)

            if cantidad <= 0:
                flash("La cantidad debe ser mayor a 0", "warning")
                return redirect(url_for("orden_bp.create"))

            # 🔥 SOLO ORDEN (SIN RECETA, SIN INVENTARIO, SIN NADA MÁS)
            orden = OrdenProduccion(
                uuid_producto=producto.uuid_producto,
                uuid_venta_detalle=None,
                cantidad_a_producir=cantidad,
                estado="Pendiente",
            )

            db.session.add(orden)
            db.session.commit()

            flash("Orden creada en estado PENDIENTE.", "success")
            return redirect(url_for("orden_bp.index"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la orden: {str(e)}", "danger")
            return redirect(url_for("orden_bp.create"))

    return render_template("produccion/orden/create.html", form=form)


@orden_bp.route("/ver/<uuid_op>")
@login_required
@roles_accepted("admin", "gerente", "produccion")
def ver(uuid_op):
    orden = (
        db.session.query(OrdenProduccion)
        .options(
            joinedload(OrdenProduccion.producto).joinedload(
                ProductoTerminado.explosion
            ),
            joinedload(OrdenProduccion.venta_detalle),
        )
        .get_or_404(uuid_op)
    )

    # Obtener ejecuciones de corte asociadas con carga ansiosa de relaciones
    cortes = (
        EjecucionCorte.query.options(
            joinedload(EjecucionCorte.rollo_usado).joinedload(RolloInventario.insumo)
        )
        .filter_by(uuid_op=uuid_op)
        .all()
    )

    return render_template("produccion/orden/ver.html", orden=orden, cortes=cortes)


@orden_bp.route("/avanzar_estado/<uuid_op>", methods=["POST"])
@login_required
@roles_accepted("admin", "gerente", "produccion")
def avanzar_estado(uuid_op):
    orden = OrdenProduccion.query.get_or_404(uuid_op)

    estados = ["Pendiente", "En Corte", "Confección", "Terminado"]

    try:
        idx_actual = estados.index(orden.estado)
        if idx_actual < len(estados) - 1:
            nuevo_estado = estados[idx_actual + 1]
            orden.estado = nuevo_estado

            # Si pasamos a Terminado, integramos al stock final
            if nuevo_estado == "Terminado":
                if orden.uuid_venta_detalle:
                    flash(
                        f"Orden terminada. Las prendas están listas para surtir la venta relacionada.",
                        "success",
                    )
                else:
                    producto = orden.producto
                    producto.stock_fisico_actual = (
                        producto.stock_fisico_actual or 0
                    ) + orden.cantidad_a_producir
                    flash(
                        f"Orden terminada. {orden.cantidad_a_producir} unidades añadidas al stock de {producto.explosion.nombre_receta}.",
                        "success",
                    )
            else:
                flash(f"Estado de la orden actualizado a {nuevo_estado}.", "success")

            db.session.commit()
        else:
            flash("La orden ya está en estado Terminado.", "info")

    except ValueError:
        flash("Estado actual inválido.", "danger")

    return redirect(url_for("orden_bp.index"))
