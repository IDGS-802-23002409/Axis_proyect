
from . import inventario_bp
from flask_security import login_required, roles_required, hash_password,roles_accepted
from .forms import InventarioForm
from flask import render_template, request
from sqlalchemy import func
from app.utils.database_connection import db
from app.models.inventario import RolloInventario, RetazoInventario
from app.models.compras import CompraDetalle, CompraEncabezado
from app.models.insumos import Insumo
from app.models.produccion import EjecucionCorte, OrdenProduccion
from app.models.explosion_materiales import ExplosionMaterialesDetalle


@inventario_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():

    #  MERMA TOTAL
    merma_total = db.session.query(
        func.coalesce(func.sum(RetazoInventario.metraje), 0)
    ).scalar()
    #  TOTAL DE METROS DE TODOS LOS ROLLOS
    total_metros_global = db.session.query(
        func.coalesce(func.sum(RolloInventario.metraje_continuo_actual), 0)
    ).scalar()

    #  SOLO INSUMOS ACTIVOS
    insumos = Insumo.query.filter_by(estatus="ACTIVO").all()

    inventario = []

    for insumo in insumos:

        total_rollos = 0
        total_metros = 0
        detalle_rollos = []

        #  SI ES ROLLO
        if insumo.unidad_medida == "ROLLO":

            total_rollos = len(insumo.rollos)

            for rollo in insumo.rollos:
                metros_actual = float(rollo.metraje_continuo_actual or 0)
                total_metros += metros_actual

                detalle_rollos.append(
                    {"uuid": rollo.uuid_rollo, "metros": metros_actual}
                )

        #  SI ES PIEZA
        elif insumo.unidad_medida == "PIEZA":
            total_metros = float(insumo.stock_total_acumulado or 0)

        #  ARMADO FINAL
        inventario.append(
            {
                "uuid_insumo": insumo.uuid_insumo,
                "nombre": insumo.nombre,
                "sku": insumo.sku,
                # tipo de compra
                "tipo": insumo.unidad_medida,
                #  CONFIGURACIÓN (CLAVE PARA TU HTML)
                "contenido": float(insumo.contenido_cantidad or 0),
                "unidad_base": insumo.contenido_unidad_medida,
                #  RESUMEN
                "stock_total": float(insumo.stock_total_acumulado or 0),
                "total_rollos": total_rollos,
                "total_metros": total_metros,
                #  DETALLE
                "rollos": detalle_rollos,
            }
        )

    return render_template(
        "produccion/inventario/index.html",
        inventario=inventario,
        merma_total=float(merma_total or 0),
        total_metros_global=float(total_metros_global or 0),
    )

@inventario_bp.route('/<uuid>')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def ver_insumo(uuid):

    # =============================
    #  INSUMO
    # =============================
    insumo = Insumo.query.get_or_404(uuid)

    # Variables base
    resumen = {}
    detalle_rollos = []
    ejecuciones = []
    retazos = []
    uso_piezas = []

    # ==========================================================
    #  CASO 1: INSUMOS POR ROLLO
    # ==========================================================
    if insumo.unidad_medida == 'ROLLO':

        #  ROLLOS
        rollos = RolloInventario.query.filter_by(uuid_insumo=uuid).all()

        total_rollos = len(rollos)

        total_metros_iniciales = sum(
            float(r.metraje_inicial or 0) for r in rollos
        )

        total_metros_actual = sum(
            float(r.metraje_continuo_actual or 0) for r in rollos
        )

        #  EJECUCIONES (uso real)
        ejecuciones = EjecucionCorte.query.join(RolloInventario).filter(
            RolloInventario.uuid_insumo == uuid
        ).all()

        total_metros_usados = sum(
            float(e.metros_sacados_bodega or 0) for e in ejecuciones
        )

        total_merma = sum(
            float(e.merma_real_calculada or 0) for e in ejecuciones
        )

        #  RETAZOS
        retazos = RetazoInventario.query.join(RolloInventario).filter(
            RolloInventario.uuid_insumo == uuid
        ).all()

        total_retazos = sum(
            float(r.metraje or 0) for r in retazos
        )

        #  DETALLE POR ROLLO
        for r in rollos:
            detalle_rollos.append({
                "uuid": r.uuid_rollo,
                "inicial": float(r.metraje_inicial or 0),
                "actual": float(r.metraje_continuo_actual or 0),
                "usado": float(r.metraje_inicial or 0) - float(r.metraje_continuo_actual or 0)
            })

        #  RESUMEN
        resumen = {
            "total_rollos": total_rollos,
            "entrada": total_metros_iniciales,
            "salida": total_metros_usados,
            "stock": total_metros_actual,
            "merma": total_merma,
            "retazos": total_retazos
        }

    # ==========================================================
    #  CASO 2: INSUMOS POR PIEZA
    # ==========================================================
    elif insumo.unidad_medida == 'PIEZA':

        #  STOCK ACTUAL
        stock_actual = float(insumo.stock_total_acumulado or 0)

        #  CONSUMO TEÓRICO (por producción)
        detalles = ExplosionMaterialesDetalle.query.filter_by(
            uuid_insumo=uuid
        ).all()

        total_usado = 0

        for d in detalles:
            producto = d.explosion.producto

            ordenes = OrdenProduccion.query.filter_by(
                uuid_producto=producto.uuid_producto
            ).all()

            for op in ordenes:
                cantidad_usada = float(d.consumo_teorico_unitario or 0) * op.cantidad_a_producir

                total_usado += cantidad_usada

                uso_piezas.append({
                    "producto": producto.nombre,
                    "orden": op.uuid_op,
                    "cantidad": cantidad_usada,
                    "fecha": op.fecha_solicitud
                })

        #  MERMA (si manejas merma en piezas, si no queda en 0)
        total_merma = 0

        #  RESUMEN
        resumen = {
            "entrada": stock_actual + total_usado,  # aproximación
            "salida": total_usado,
            "stock": stock_actual,
            "merma": total_merma
        }


    return render_template(
        "produccion/inventario/ver.html",
        insumo=insumo,
        resumen=resumen,
        rollos=detalle_rollos,
        ejecuciones=ejecuciones,
        uso_piezas=uso_piezas
    )