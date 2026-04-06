"""
routes.py · Blueprint: prendas
Módulo de Costo y Utilidad — SOLO LECTURA

Lógica de precio:
  Para cada insumo del BOM, se toman las últimas 5 compras (CompraDetalle
  ordenadas por fecha_compra DESC) y se calcula el precio promedio.
  Ese precio promedio × consumo_teorico_unitario = costo real del insumo.
  La suma de todos los insumos = COGS de la prenda.
  Margen = (precio_venta - COGS) / precio_venta × 100
"""
from flask import render_template, flash, redirect, url_for
from flask_security import login_required, roles_required, roles_accepted
from . import prendas_bp
from app.utils.database_connection import db
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.models.explosion_materiales import (
    ExplosionMaterialesCabecera,
    ExplosionMaterialesDetalle,
)
from app.models.compras import CompraDetalle, CompraEncabezado
from app.models.insumos import Insumo
from sqlalchemy import func


# ══════════════════════════════════════════════════════════════════════════════
# HELPER PRINCIPAL: precio promedio de las últimas N compras de un insumo
# ══════════════════════════════════════════════════════════════════════════════

def _precio_promedio_insumo(uuid_insumo: str, n: int = 5) -> float:
    """
    Devuelve el promedio de costo_unitario_compra de las últimas N compras
    del insumo. Si no hay compras registradas usa el costo_unitario_individual
    del catálogo de insumos como fallback.
    """
    ultimas = (
        db.session.query(CompraDetalle.costo_unitario_compra)
        .join(CompraEncabezado,
              CompraDetalle.uuid_compra == CompraEncabezado.uuid_compra)
        .filter(
            CompraDetalle.uuid_insumo == uuid_insumo,
            CompraEncabezado.estatus  == 'Recibido',   # solo compras confirmadas
        )
        .order_by(CompraEncabezado.fecha_compra.desc())
        .limit(n)
        .all()
    )

    if ultimas:
        precios = [float(r.costo_unitario_compra) for r in ultimas]
        return round(sum(precios) / len(precios), 4)

    # Fallback: costo del catálogo
    insumo = db.session.get(Insumo, uuid_insumo)
    return float(insumo.costo_unitario_individual) if insumo else 0.0


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: construir BOM enriquecido con precio promedio real
# ══════════════════════════════════════════════════════════════════════════════

def _get_bom_con_precios(uuid_producto: str) -> tuple[list[dict], float]:
    """
    Lee la explosión de materiales y calcula el subtotal de cada insumo
    usando el precio promedio de sus últimas 5 compras.

    Retorna:
        bom   : lista de dicts para el template
        total : suma total del costo de insumos ($)
    """
    cabecera = (
        ExplosionMaterialesCabecera.query
        .filter_by(uuid_producto=uuid_producto)
        .first()
    )
    if not cabecera:
        return [], 0.0

    filas = (
        db.session.query(ExplosionMaterialesDetalle, Insumo)
        .join(Insumo, ExplosionMaterialesDetalle.uuid_insumo == Insumo.uuid_insumo)
        .filter(ExplosionMaterialesDetalle.uuid_explosion == cabecera.uuid_explosion)
        .order_by(Insumo.nombre)
        .all()
    )

    bom   = []
    total = 0.0

    for det, ins in filas:
        consumo       = float(det.consumo_teorico_unitario)
        precio_prom   = _precio_promedio_insumo(ins.uuid_insumo)
        subtotal      = round(consumo * precio_prom, 2)
        total        += subtotal

        # Historial de las últimas 5 compras para mostrar en tooltip / detalle
        historial = (
            db.session.query(
                CompraDetalle.costo_unitario_compra,
                CompraEncabezado.fecha_compra,
            )
            .join(CompraEncabezado,
                  CompraDetalle.uuid_compra == CompraEncabezado.uuid_compra)
            .filter(
                CompraDetalle.uuid_insumo == ins.uuid_insumo,
                CompraEncabezado.estatus  == 'Recibido',
            )
            .order_by(CompraEncabezado.fecha_compra.desc())
            .limit(5)
            .all()
        )

        bom.append({
            "nombre_insumo" : ins.nombre,
            "categoria"     : ins.categoria.nombre if ins.categoria else "—",
            "consumo"       : consumo,
            "ancho"         : float(det.ancho_referencia) if det.ancho_referencia else None,
            "precio_promedio": precio_prom,
            "subtotal"      : subtotal,
            "historial"     : [
                {
                    "precio": float(h.costo_unitario_compra),
                    "fecha" : h.fecha_compra.strftime('%d/%m/%y') if h.fecha_compra else "—",
                }
                for h in historial
            ],
            "n_compras"     : len(historial),   # cuántas compras reales hay
        })

    return bom, round(total, 2)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: resumen financiero completo
# ══════════════════════════════════════════════════════════════════════════════

def _calcular_resumen(producto: ProductoTerminado,
                      bom: list[dict],
                      costo_insumos: float) -> dict:
    """
    Construye el dict de rentabilidad que consume el template.
    costo_confeccion = 0 hasta que se agregue el campo al modelo.
    """
    costo_confeccion = 0.0
    cogs             = round(costo_insumos + costo_confeccion, 2)
    precio           = float(producto.precio_venta)
    utilidad         = round(precio - cogs, 2)
    margen_pct       = round((utilidad / precio) * 100, 2) if precio > 0 else 0.0

    return {
        "costo_insumos"   : costo_insumos,
        "costo_confeccion": costo_confeccion,
        "cogs"            : cogs,
        "precio_venta"    : precio,
        "utilidad_neta"   : utilidad,
        "margen_pct"      : margen_pct,
        "num_materiales"  : len(bom),
    }


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: lista lateral con margen precalculado
# ══════════════════════════════════════════════════════════════════════════════

def _sidebar_prendas() -> list:
    try:
        rows = (
            db.session.query(ProductoTerminado, ModeloRopa)
            .join(ModeloRopa)
            .order_by(ModeloRopa.nombre_modelo, ProductoTerminado.talla)
            .all()
        )
        print(f"[DEBUG] Prendas encontradas: {len(rows)}", flush=True)
        result = []
        for pt, mr in rows:
            try:
                bom, costo_ins   = _get_bom_con_precios(pt.uuid_producto)
                resumen          = _calcular_resumen(pt, bom, costo_ins)
                pt.nombre_modelo = mr.nombre_modelo
                pt.margen_pct    = resumen["margen_pct"]
                result.append(pt)
            except Exception as e:
                print(f"[DEBUG] Error en prenda {pt.uuid_producto}: {e}", flush=True)
        return result
    except Exception as e:
        print(f"[DEBUG] Error en query principal: {e}", flush=True)
        return []


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@prendas_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():
    """Vista de entrada — sin prenda seleccionada."""
    try:
        prendas = _sidebar_prendas()
        return render_template(
            'prendas/index.html',
            prendas        = prendas,
            prenda_activa  = None,
            bom_activo     = [],
            resumen_costos = {},
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cargar el módulo: {str(e)}", "danger")
        return render_template('prendas/index.html',
                               prendas=[], prenda_activa=None,
                               bom_activo=[], resumen_costos={})


@prendas_bp.route('/<uuid_producto>')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def detalle(uuid_producto: str):
    """Reporte de costo y utilidad de una prenda específica."""
    try:
        pt, mr = (
            db.session.query(ProductoTerminado, ModeloRopa)
            .join(ModeloRopa)
            .filter(
                ProductoTerminado.uuid_producto == uuid_producto,
            )
            .first_or_404()
        )
        pt.nombre_modelo = mr.nombre_modelo
        pt.coleccion     = getattr(mr, "coleccion", None)

        bom_activo, costo_insumos = _get_bom_con_precios(uuid_producto)
        resumen_costos            = _calcular_resumen(pt, bom_activo, costo_insumos)
        prendas                   = _sidebar_prendas()

        return render_template(
            'prendas/index.html',
            prendas        = prendas,
            prenda_activa  = pt,
            bom_activo     = bom_activo,
            resumen_costos = resumen_costos,
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('prendas.index'))