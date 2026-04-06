from flask import flash, redirect, render_template, request, url_for
from app.blueprints.orden_produccion import orden_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado, ModeloRopa

from app.utils.database_connection import db
from flask_security import login_required, roles_accepted
from decimal import Decimal
from app.models.explosion_materiales import ExplosionMaterialesDetalle
from app.models.inventario import RolloInventario
from app.models.produccion import OrdenProduccion, EjecucionCorte
from app.models.ventas import VentaEncabezado,VentaDetalle
from app.utils.database_connection import db
from .forms import OrdenProduccionForm

@orden_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():

    ordenes = db.session.query(OrdenProduccion).join(
        ProductoTerminado
    ).join(
        ModeloRopa
    ).order_by(OrdenProduccion.fecha_solicitud.desc()).all()

    return render_template(
        'produccion/orden/index.html',
        ordenes=ordenes
    )




@orden_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def create():

    form = OrdenProduccionForm()

    # Productos activos
    productos = ProductoTerminado.query.filter_by(active=True).all()
    form.uuid_producto.choices = [
        (p.uuid_producto, f"{p.sku_especifico} - {p.modelo.nombre_modelo} ({p.talla})")
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
        if uuid_venta:
            venta = VentaDetalle.query.get(uuid_venta)
            if not venta:
                flash("La venta seleccionada no existe", "danger")
                return redirect(url_for('orden_bp.index'))
            cantidad = int(venta.cantidad)
            tipo = 'PEDIDO'
        else:
            cantidad = int(form.cantidad_a_producir.data)
            tipo = 'STOCK'

        try:
            # Crear orden
            orden = OrdenProduccion(
                uuid_producto=producto.uuid_producto,
                uuid_venta_detalle=uuid_venta,
                cantidad_a_producir=cantidad
            )
            db.session.add(orden)
            db.session.flush()  # tener uuid_op

            # Consumir insumos por receta
            for detalle in producto.explosion.detalles:

                consumo_unitario = Decimal(detalle.consumo_teorico_unitario)
                prendas_restantes = cantidad

                # Solo rollos con metraje disponible > 0
                rollos = RolloInventario.query.filter(
                    RolloInventario.uuid_insumo == detalle.uuid_insumo,
                    RolloInventario.metraje_continuo_actual > 0
                ).order_by(RolloInventario.fecha_creacion.asc()).all()

                if not rollos:
                    raise Exception(f"No hay rollos disponibles para el insumo {detalle.insumo.nombre_insumo}")

                for rollo in rollos:

                    metraje_disponible = Decimal(rollo.metraje_continuo_actual)
                    prendas_de_este_rollo = int(metraje_disponible // consumo_unitario)

                    if prendas_de_este_rollo <= 0:
                        continue

                    prendas_a_usar = min(prendas_restantes, prendas_de_este_rollo)
                    metros_a_descontar = Decimal(prendas_a_usar) * consumo_unitario

                    #  Descontar del rollo
                    rollo.metraje_continuo_actual -= metros_a_descontar

                    # Normalizar rollos a 0 si queda muy poco
                    if rollo.metraje_continuo_actual <= Decimal('0.0001'):
                        rollo.metraje_continuo_actual = Decimal('0.0000')

                    #  Registrar ejecución de corte
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
                    raise Exception(f"No hay suficiente tela para completar la producción de {producto.sku_especifico}")

            db.session.commit()

            flash(
                "Orden creada desde venta correctamente" if tipo == 'PEDIDO'
                else "Orden creada para stock correctamente",
                "success"
            )
            return redirect(url_for('orden_bp.index'))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")
            return redirect(url_for('orden_bp.index'))

    return render_template('produccion/orden/create.html', form=form)