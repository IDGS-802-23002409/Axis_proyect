from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, roles_required, roles_accepted

from app.blueprints.costo_utilidad import costo_utilidad_bp
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import (
    ExplosionMaterialesCabecera,
    ExplosionMaterialesDetalle,
)
from app.models.compras import CompraEncabezado, CompraDetalle
from app.models.produccion import EjecucionCorte, OrdenProduccion, MermaPiezas
from app.utils.database_connection import db

def _obtener_costo_promedio_insumo(uuid_insumo, cache_costos=None):
    """
    Costo promedio ponderado por unidad base,
    usando las últimas 5 compras RECIBIDAS del insumo.

    Fórmula:
        total_gastado / total_unidades_base_compradas
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

    total_costo = 0.0
    total_unidades_base = 0.0

    for d in detalles:
        if (
            d.costo_unitario_compra is not None
            and d.cantidad_comprada is not None
            and d.insumo is not None
            and d.insumo.contenido_cantidad is not None
            and float(d.insumo.contenido_cantidad) > 0
        ):
            cantidad_comprada    = float(d.cantidad_comprada)
            costo_unitario_compra = float(d.costo_unitario_compra)
            contenido_cantidad   = float(d.insumo.contenido_cantidad)

            total_costo          += cantidad_comprada * costo_unitario_compra
            total_unidades_base  += cantidad_comprada * contenido_cantidad

    if total_unidades_base == 0:
        if cache_costos is not None:
            cache_costos[uuid_insumo] = 0.0
        return 0.0

    costo_promedio = total_costo / total_unidades_base

    if cache_costos is not None:
        cache_costos[uuid_insumo] = costo_promedio

    return costo_promedio

def _obtener_merma_promedio_tela(uuid_producto):
    """
    Merma promedio ponderada de tela (METRO) para el producto,
    basada en EjecucionCorte.

    Fórmula:
        sum(merma_real_calculada) / sum(metros_teoricos_requeridos)

    Retorna decimal: 0.10 = 10 %
    """
    ejecuciones = (
        EjecucionCorte.query
        .join(OrdenProduccion)
        .filter(OrdenProduccion.uuid_producto == uuid_producto)
        .all()
    )

    if not ejecuciones:
        return 0.0

    total_merma_real    = 0.0
    total_metros_teoricos = 0.0

    for e in ejecuciones:
        if (
            e.merma_real_calculada is not None
            and e.metros_teoricos_requeridos is not None
            and float(e.metros_teoricos_requeridos) > 0
        ):
            total_merma_real      += float(e.merma_real_calculada)
            total_metros_teoricos += float(e.metros_teoricos_requeridos)

    if total_metros_teoricos == 0:
        return 0.0

    return total_merma_real / total_metros_teoricos


def _obtener_merma_promedio_pieza(uuid_producto, uuid_insumo):
    """
    Merma promedio ponderada de un insumo tipo PIEZA para el producto,
    basada en MermaPiezas.

    Fórmula:
        sum(cantidad_real_consumida - cantidad_teorica) / sum(cantidad_teorica)

    Retorna decimal: 0.05 = 5 %
    Puede ser negativo si históricamente se consume menos de lo teórico.
    """
    registros = (
        MermaPiezas.query
        .join(OrdenProduccion)
        .filter(
            OrdenProduccion.uuid_producto == uuid_producto,
            MermaPiezas.uuid_insumo == uuid_insumo,
        )
        .all()
    )

    if not registros:
        return 0.0

    total_diferencia = 0.0
    total_teorico    = 0.0

    for r in registros:
        if (
            r.cantidad_real_consumida is not None
            and r.cantidad_teorica is not None
            and float(r.cantidad_teorica) > 0
        ):
            total_diferencia += float(r.cantidad_real_consumida) - float(r.cantidad_teorica)
            total_teorico    += float(r.cantidad_teorica)

    if total_teorico == 0:
        return 0.0

    return total_diferencia / total_teorico

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

def _calcular_costo_mp(producto, merma_tela=0.0, mermas_pieza=None):
    """
    Costo total de materia prima por unidad producida.

    - Insumos METRO  → consumo teórico ajustado con merma_tela
    - Insumos PIEZA  → consumo teórico ajustado con merma histórica por insumo
                       (si no hay historial, se usa el teórico puro)
    """
    if mermas_pieza is None:
        mermas_pieza = {}

    _, detalles = _obtener_explosion_y_detalles(producto)
    if not detalles:
        return 0.0

    costo_mp     = 0.0
    cache_costos = {}

    for d in detalles:
        insumo = d.insumo
        if not insumo:
            continue

        costo_promedio  = _obtener_costo_promedio_insumo(insumo.uuid_insumo, cache_costos)
        consumo_teorico = float(d.consumo_teorico_unitario or 0)

        if insumo.contenido_unidad_medida == "METRO":
            consumo_real = consumo_teorico * (1 + merma_tela)
        else:
            merma_pieza  = mermas_pieza.get(insumo.uuid_insumo, 0.0)
            consumo_real = consumo_teorico * (1 + merma_pieza)

        costo_mp += consumo_real * costo_promedio

    return costo_mp


def _obtener_desglose_insumos(producto, merma_tela=0.0, mermas_pieza=None):
    """
    Desglose línea a línea de cada insumo con su costo y merma aplicada.
    """
    if mermas_pieza is None:
        mermas_pieza = {}

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

        if insumo.contenido_unidad_medida == "METRO":
            merma_aplicada = merma_tela
            consumo_real   = consumo_teorico * (1 + merma_aplicada)
        else:
            merma_aplicada = mermas_pieza.get(insumo.uuid_insumo, 0.0)
            consumo_real   = consumo_teorico * (1 + merma_aplicada)

        desglose.append({
            "insumo":           insumo.nombre or "N/A",
            "unidad_base":      insumo.contenido_unidad_medida,
            "consumo_teorico":  consumo_teorico,
            "consumo_real":     consumo_real,
            "merma_aplicada_%": merma_aplicada * 100,
            "costo_unitario":   costo_promedio,
            "costo_total":      consumo_real * costo_promedio,
            "fuente_merma":     "corte" if insumo.contenido_unidad_medida == "METRO" else "produccion",
        })

    return desglose


def _construir_mermas_pieza(producto, detalles_explosion):
    """
    Precalcula el dict {uuid_insumo: merma_decimal} para todos los insumos
    PIEZA del producto. Se llama una sola vez por request para no repetir
    queries dentro de los loops de costo y desglose.
    """
    mermas = {}
    for d in detalles_explosion:
        insumo = d.insumo
        if insumo and insumo.contenido_unidad_medida != "METRO":
            mermas[insumo.uuid_insumo] = _obtener_merma_promedio_pieza(
                producto.uuid_producto,
                insumo.uuid_insumo,
            )
    return mermas

@costo_utilidad_bp.route("/costo-utilidad", methods=["GET"])
@login_required
@roles_accepted('admin', 'gerente')
def index():
    productos = ProductoTerminado.query.order_by(
        ProductoTerminado.uuid_modelo,
        ProductoTerminado.talla
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

    product         = None
    costo_mp        = 0.0
    margen          = 0.0
    utilidad_actual = 0.0
    precio_ajustado = 0.0
    desglose_insumos = []
    merma_tela      = 0.0
    mermas_pieza    = {}   # {uuid_insumo: decimal} — disponible en template si se necesita

    if request.method == "GET":
        uuid_producto_param = (
            request.args.get("producto") or uuid_producto or ""
        ).strip()

        if uuid_producto_param:
            product = ProductoTerminado.query.filter_by(
                uuid_producto=uuid_producto_param
            ).first()

            if product:
                _, detalles = _obtener_explosion_y_detalles(product)

                merma_tela   = _obtener_merma_promedio_tela(product.uuid_producto)
                mermas_pieza = _construir_mermas_pieza(product, detalles)

                costo_mp         = _calcular_costo_mp(product, merma_tela, mermas_pieza)
                desglose_insumos = _obtener_desglose_insumos(product, merma_tela, mermas_pieza)

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
                        "No fue posible calcular el costo del producto. "
                        "Verifica compras recibidas, contenido del insumo y consumos configurados.",
                        "warning",
                    )

    if request.method == "POST":
        uuid_producto_post = (request.form.get("producto") or "").strip()

        product = ProductoTerminado.query.filter_by(
            uuid_producto=uuid_producto_post
        ).first()

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
                "error"
            )
            return redirect(
                url_for("costo_utilidad.detalle", uuid_producto=product.uuid_producto)
            )

        merma_tela   = _obtener_merma_promedio_tela(product.uuid_producto)
        mermas_pieza = _construir_mermas_pieza(product, detalles)

        costo_mp         = _calcular_costo_mp(product, merma_tela, mermas_pieza)
        desglose_insumos = _obtener_desglose_insumos(product, merma_tela, mermas_pieza)

        if costo_mp == 0.0:
            flash(
                "No fue posible calcular el costo del producto. "
                "Verifica compras recibidas, contenido del insumo y consumos configurados.",
                "error"
            )
            return redirect(
                url_for("costo_utilidad.detalle", uuid_producto=product.uuid_producto)
            )

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
                f"Precio actualizado a ${precio_ajustado:.2f} para {product.sku_especifico}",
                "success",
            )

            return redirect(
                url_for("costo_utilidad.detalle", uuid_producto=product.uuid_producto)
            )

    return render_template(
        "produccion/costo_utilidad/detalle.html",
        productos=productos,
        producto=product,
        costo_mp=costo_mp,
        margen=margen,
        utilidad_actual=utilidad_actual,
        precio_ajustado=precio_ajustado,
        desglose_insumos=desglose_insumos,
        merma_tela=merma_tela * 100,
        mermas_pieza={k: v * 100 for k, v in mermas_pieza.items()},
    )