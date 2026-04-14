from . import inventario_bp
from flask_security import login_required, roles_accepted
from flask import render_template
from sqlalchemy import func
from app.utils.database_connection import db
from app.models.inventario import RolloInventario
from app.models.insumos import Insumo
from app.models.produccion import EjecucionCorte, OrdenProduccion
from app.models.explosion_materiales import ExplosionMaterialesDetalle
from app.models.produccion import OrdenProduccion, EjecucionCorte, EjecucionCorteRollo
from app.models.insumos import Insumo
from app.models.inventario import RolloInventario
from app.models.modelos_productos import ProductoTerminado
from app.models.mermas import Merma


@inventario_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():

    total_metros_global = db.session.query(
        func.coalesce(func.sum(RolloInventario.metraje_continuo_actual), 0)
    ).scalar()

    # Merma total de tela activa (tipo TELA, activo=True)
    merma_tela_global = db.session.query(
        func.coalesce(func.sum(Merma.cantidad), 0)
    ).filter(
        Merma.tipo_merma == 'TELA',
        Merma.activo == True
    ).scalar()

    insumos    = Insumo.query.filter_by(estatus="ACTIVO").all()
    inventario = []

    for insumo in insumos:
        total_rollos   = 0
        total_metros   = 0
        detalle_rollos = []

        if insumo.unidad_medida == "ROLLO":
            total_rollos = len(insumo.rollos)
            for rollo in insumo.rollos:
                metros_actual = float(rollo.metraje_continuo_actual or 0)
                total_metros += metros_actual
                detalle_rollos.append({
                    "uuid":   rollo.uuid_rollo,
                    "metros": metros_actual,
                })

        elif insumo.unidad_medida == "PIEZA":
            total_metros = float(insumo.stock_total_acumulado or 0)

        inventario.append({
            "uuid_insumo":  insumo.uuid_insumo,
            "nombre":       insumo.nombre,
            "sku":          insumo.sku,
            "tipo":         insumo.unidad_medida,
            "contenido":    float(insumo.contenido_cantidad or 0),
            "unidad_base":  insumo.contenido_unidad_medida,
            "stock_total":  float(insumo.stock_total_acumulado or 0),
            "total_rollos": total_rollos,
            "total_metros": total_metros,
            "rollos":       detalle_rollos,
        })

    return render_template(
        "produccion/inventario/index.html",
        inventario=inventario,
        total_metros_global=float(total_metros_global or 0),
        merma_tela_global=float(merma_tela_global or 0),
    )

@inventario_bp.route('/<uuid>')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def ver_insumo(uuid):

    insumo = Insumo.query.get_or_404(uuid)

    resumen        = {}
    detalle_rollos = []
    ejecuciones    = []
    uso_piezas     = []
    mermas         = []

    if insumo.unidad_medida == 'ROLLO':

        rollos = RolloInventario.query.filter_by(uuid_insumo=uuid).all()

        total_metros_iniciales = sum(float(r.metraje_inicial or 0) for r in rollos)
        total_metros_actual    = sum(float(r.metraje_continuo_actual or 0) for r in rollos)

        #  JOIN CORRECTO (usando tabla puente)
        ejecuciones = (
            db.session.query(EjecucionCorte)
            .join(EjecucionCorteRollo, EjecucionCorte.uuid_corte == EjecucionCorteRollo.uuid_corte)
            .join(RolloInventario, EjecucionCorteRollo.uuid_rollo == RolloInventario.uuid_rollo)
            .filter(RolloInventario.uuid_insumo == uuid)
            .all()
        )

        #  TOTAL REAL USADO (desde tabla puente)
        total_metros_usados = (
            db.session.query(func.sum(EjecucionCorteRollo.metros_usados))
            .join(RolloInventario, EjecucionCorteRollo.uuid_rollo == RolloInventario.uuid_rollo)
            .filter(RolloInventario.uuid_insumo == uuid)
            .scalar()
        ) or 0

        #  Mermas
        uuid_rollos = [r.uuid_rollo for r in rollos]

        if uuid_rollos:
            mermas = (
                Merma.query
                .filter(
                    Merma.tipo_merma == 'TELA',
                    Merma.uuid_rollo.in_(uuid_rollos),
                    Merma.activo == True
                )
                .order_by(Merma.fecha_creacion.desc())
                .all()
            )
        else:
            mermas = []

        total_merma = sum(float(m.cantidad or 0) for m in mermas)

        #  Detalle por rollo
        for r in rollos:
            detalle_rollos.append({
                "uuid":    r.uuid_rollo,
                "inicial": float(r.metraje_inicial or 0),
                "actual":  float(r.metraje_continuo_actual or 0),
                "usado":   float(r.metraje_inicial or 0) - float(r.metraje_continuo_actual or 0),
            })

        resumen = {
            "total_rollos": len(rollos),
            "entrada":      total_metros_iniciales,
            "salida":       float(total_metros_usados),
            "stock":        total_metros_actual,
            "merma":        total_merma,
        }

    elif insumo.unidad_medida == 'PIEZA':

        stock_actual = float(insumo.stock_total_acumulado or 0)
        detalles     = ExplosionMaterialesDetalle.query.filter_by(uuid_insumo=uuid).all()
        total_usado  = 0

        for d in detalles:
            for producto in d.explosion.productos:
                ordenes = OrdenProduccion.query.filter_by(
                    uuid_producto=producto.uuid_producto
                ).all()

                for op in ordenes:
                    cantidad_usada = float(d.consumo_teorico_unitario or 0) * op.cantidad_a_producir
                    total_usado   += cantidad_usada

                    uso_piezas.append({
                        "producto": producto.nombre_display,
                        "sku":      producto.sku_especifico,
                        "orden":    op.uuid_op[:8] + "…",
                        "estado":   op.estado,
                        "cantidad": cantidad_usada,
                        "fecha":    op.fecha_solicitud,
                    })

        #  Mermas de insumo
        mermas = (
            Merma.query
            .filter(
                Merma.tipo_merma == 'INSUMO',
                Merma.uuid_insumo == uuid,
                Merma.activo == True
            )
            .order_by(Merma.fecha_creacion.desc())
            .all()
        )

        total_merma = sum(float(m.cantidad or 0) for m in mermas)

        resumen = {
            "entrada": stock_actual + total_usado,
            "salida":  total_usado,
            "stock":   stock_actual,
            "merma":   total_merma,
        }

    return render_template(
        "produccion/inventario/ver.html",
        insumo=insumo,
        resumen=resumen,
        rollos=detalle_rollos,
        ejecuciones=ejecuciones,
        uso_piezas=uso_piezas,
        mermas=mermas,
    )