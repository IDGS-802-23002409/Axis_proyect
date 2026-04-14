from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, roles_accepted

from app.blueprints.costo_utilidad import costo_utilidad_bp
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import (
    ExplosionMaterialesCabecera,
    ExplosionMaterialesDetalle,
)
from app.models.compras import CompraEncabezado, CompraDetalle
from app.utils.database_connection import db


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _obtener_costo_promedio_insumo(uuid_insumo, cache_costos=None):
    """
    Costo promedio ponderado por unidad base,
    usando las últimas 5 compras RECIBIDAS del insumo.

    Fórmula: total_gastado / total_unidades_base_compradas
    """
    if cache_costos is not None and uuid_insumo in cache_costos:
        return cache_costos[uuid_insumo]

    detalles = (
        CompraDetalle.query
        .join(CompraEncabezado)
        .filter(
            CompraDetalle.uuid_insumo == uuid_insumo,
            CompraEncabezado.estatus == "RECIBIDO"
        )
        .order_by(CompraEncabezado.fecha_compra.desc())
        .limit(5)
        .all()
    )

    if not detalles:
        if cache_costos is not None:
            cache_costos[uuid_insumo] = 0.0
        return 0.0

    total_costo         = 0.0
    total_unidades_base = 0.0

    for d in detalles:
        if (
            d.costo_unitario_compra is not None
            and d.cantidad_comprada is not None
            and d.insumo is not None
        ):
            # TOTAL COST: Siempre es cantidad * costo_unitario (ya ajustado en la recepción)
            total_costo += float(d.cantidad_comprada) * float(d.costo_unitario_compra)
            
            # TOTAL UNITS: Para rollos, usamos el metraje real inicial. Para piezas, la cantidad.
            if d.insumo.unidad_medida == "ROLLO":
                # Sumar metraje inicial de todos los rollos vinculados a este detalle
                # Esto es más preciso que usar insumo.contenido_cantidad
                metraje_real_lote = sum(float(r.metraje_inicial or 0) for r in d.rollos)
                if metraje_real_lote > 0:
                    total_unidades_base += metraje_real_lote
                else:
                    # Fallback si no hay rollos registrados (no debería pasar en RECIBIDO)
                    total_unidades_base += float(d.cantidad_comprada) * float(d.insumo.contenido_cantidad or 0)
            else:
                total_unidades_base += float(d.cantidad_comprada)

    costo_promedio = total_costo / total_unidades_base if total_unidades_base > 0 else 0.0

    if cache_costos is not None:
        cache_costos[uuid_insumo] = costo_promedio

    return costo_promedio


def _obtener_explosion_y_detalles(producto):
    if not producto.uuid_explosion:
        return None, []

    cabecera = ExplosionMaterialesCabecera.query.get(producto.uuid_explosion)
    if not cabecera:
        return None, []

    detalles = ExplosionMaterialesDetalle.query.filter_by(
        uuid_explosion=cabecera.uuid_explosion
    ).all()

    return cabecera, detalles


def _calcular_costo_mp(producto):
    """
    Costo total de materia prima por unidad producida,
    usando exclusivamente el consumo teórico de la explosión
    de materiales — sin aplicar ningún factor de merma.
    """
    _, detalles = _obtener_explosion_y_detalles(producto)
    if not detalles:
        return 0.0

    costo_mp     = 0.0
    cache_costos = {}

    for d in detalles:
        if not d.insumo:
            continue

        costo_promedio  = _obtener_costo_promedio_insumo(d.insumo.uuid_insumo, cache_costos)
        consumo_teorico = float(d.consumo_teorico_unitario or 0)
        costo_mp       += consumo_teorico * costo_promedio

    return costo_mp


def _obtener_desglose_insumos(producto):
    """
    Desglose línea a línea de cada insumo con su consumo
    teórico y costo — sin merma aplicada.
    """
    _, detalles = _obtener_explosion_y_detalles(producto)
    if not detalles:
        return []

    desglose     = []
    cache_costos = {}

    for d in detalles:
        insumo = d.insumo
        if not insumo:
            continue

        costo_promedio  = _obtener_costo_promedio_insumo(insumo.uuid_insumo, cache_costos)
        consumo_teorico = float(d.consumo_teorico_unitario or 0)

        desglose.append({
            "insumo":          insumo.nombre or "N/A",
            "unidad_base":     insumo.contenido_unidad_medida,
            "consumo_teorico": consumo_teorico,
            "costo_unitario":  costo_promedio,
            "costo_total":     consumo_teorico * costo_promedio,
        })

    return desglose


# ─────────────────────────────────────────────
#  VISTAS
# ─────────────────────────────────────────────

@costo_utilidad_bp.route("/costo-utilidad", methods=["GET"])
@login_required
@roles_accepted('admin', 'gerente')
def index():
    productos = ProductoTerminado.query.order_by(
        ProductoTerminado.uuid_explosion,
        ProductoTerminado.sku_especifico
    ).all()

    return render_template(
        "produccion/costo_utilidad/lista.html",
        productos=productos,
    )


@costo_utilidad_bp.route("/costo-utilidad/<uuid_producto>", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente')
def detalle(uuid_producto):
    productos = ProductoTerminado.query.order_by(
        ProductoTerminado.fecha_actualizacion.desc()
    ).all()

    product          = None
    costo_mp         = 0.0
    margen           = 0.0
    utilidad_actual  = 0.0
    precio_ajustado  = 0.0
    desglose_insumos = []

    # ── GET ──────────────────────────────────
    if request.method == "GET":
        uuid_param = (request.args.get("producto") or uuid_producto or "").strip()

        if uuid_param:
            product = ProductoTerminado.query.filter_by(uuid_producto=uuid_param).first()

            if product:
                _, detalles = _obtener_explosion_y_detalles(product)
                costo_mp         = _calcular_costo_mp(product)
                desglose_insumos = _obtener_desglose_insumos(product)

                try:
                    precio_actual = float(product.precio_venta or 0)
                except (TypeError, ValueError):
                    precio_actual = 0.0

                utilidad_actual = (
                    ((precio_actual - costo_mp) / costo_mp) * 100
                    if costo_mp > 0 else 0.0
                )

                if not detalles:
                    flash(
                        "Este producto no tiene explosión de materiales configurada.",
                        "warning",
                    )
                elif costo_mp == 0.0:
                    flash(
                        "No fue posible calcular el costo. "
                        "Verifica que el producto tenga compras recibidas "
                        "y consumos configurados en su receta.",
                        "warning",
                    )

    # ── POST — calcular precio sugerido y opcionalmente guardarlo ──
    elif request.method == "POST":
        uuid_post = (request.form.get("producto") or "").strip()
        product   = ProductoTerminado.query.filter_by(uuid_producto=uuid_post).first()

        if not product:
            flash("Producto no encontrado.", "error")
            return redirect(url_for("costo_utilidad.index"))

        try:
            margen = float(request.form.get("margen", 0) or 0)
        except ValueError:
            margen = 0.0

        _, detalles = _obtener_explosion_y_detalles(product)

        if not detalles:
            flash(
                "Este producto no tiene explosión de materiales configurada.",
                "error",
            )
            return redirect(url_for("costo_utilidad.detalle", uuid_producto=uuid_post))

        costo_mp         = _calcular_costo_mp(product)
        desglose_insumos = _obtener_desglose_insumos(product)

        if costo_mp == 0.0:
            flash(
                "No fue posible calcular el costo. "
                "Verifica compras recibidas y consumos configurados.",
                "error",
            )
            return redirect(url_for("costo_utilidad.detalle", uuid_producto=uuid_post))

        try:
            precio_actual = float(product.precio_venta or 0)
        except (TypeError, ValueError):
            precio_actual = 0.0

        utilidad_actual = (
            ((precio_actual - costo_mp) / costo_mp) * 100
            if costo_mp > 0 else 0.0
        )

        precio_ajustado = costo_mp * (1 + (margen / 100))

        if request.form.get("guardar_precio") == "1":
            product.precio_venta = precio_ajustado
            db.session.commit()
            flash(
                f"Precio actualizado a ${precio_ajustado:.2f} "
                f"para {product.sku_especifico}.",
                "success",
            )
            return redirect(url_for("costo_utilidad.detalle", uuid_producto=uuid_post))

    return render_template(
        "produccion/costo_utilidad/detalle.html",
        productos=productos,
        producto=product,
        costo_mp=costo_mp,
        margen=margen,
        utilidad_actual=utilidad_actual,
        precio_ajustado=precio_ajustado,
        desglose_insumos=desglose_insumos,
    )