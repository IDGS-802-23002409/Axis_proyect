from . import inventario_bp
from .forms import InventarioForm

from app.models.inventario import RolloInventario, RetazoInventario
from app.models.compras import CompraDetalle, CompraEncabezado
from app.models.insumos import Insumo
from app.models.produccion import EjecucionCorte

from app.utils.database_connection import db

from flask import render_template, request

from flask import Blueprint, render_template
from app.models import Insumo, RolloInventario
from sqlalchemy import func



@inventario_bp.route('/')
def index():
    insumos = Insumo.query.filter_by(estatus='ACTIVO').all()

    inventario = []

    for insumo in insumos:

        # Solo aplica para rollos
        total_rollos = 0
        total_metros = 0
        detalle_rollos = []

        if insumo.unidad_medida == 'ROLLO':
            total_rollos = len(insumo.rollos)

            for rollo in insumo.rollos:
                metros_actual = float(rollo.metraje_continuo_actual or 0)

                total_metros += metros_actual

                detalle_rollos.append({
                    "uuid": rollo.uuid_rollo,
                    "metros": metros_actual
                })

        inventario.append({
            "nombre": insumo.nombre,
            "sku": insumo.sku,
            "tipo": insumo.unidad_medida,
            "unidad": insumo.contenido_unidad_medida,

            #  resumen
            "total_rollos": total_rollos,
            "total_metros": total_metros,

            # detalle
            "rollos": detalle_rollos
        })

    return render_template("produccion/inventario/index.html", inventario=inventario)

'''

@inventario_bp.route("/", methods=["GET", "POST"])
def index():

    form = InventarioForm()

    #  llenar select de insumos
    form.uuid_insumo.choices = [("", "Todos")] + [
        (i.uuid_insumo, f"{i.sku} - {i.nombre}")
        for i in Insumo.query.all()
    ]

    movimientos = []

    # =========================
    #  ENTRADAS (COMPRAS)
    # =========================
    compras = (
        db.session.query(CompraDetalle, CompraEncabezado, Insumo)
        .join(CompraEncabezado, CompraDetalle.uuid_compra == CompraEncabezado.uuid_compra)
        .join(Insumo, CompraDetalle.uuid_insumo == Insumo.uuid_insumo)
        .filter(CompraEncabezado.estatus == 'RECIBIDO')
    )

    # =========================
    #  SALIDAS - CONSUMO
    # =========================
    cortes = (
        db.session.query(EjecucionCorte, RolloInventario, Insumo)
        .join(RolloInventario, EjecucionCorte.uuid_rollo_usado == RolloInventario.uuid_rollo)
        .join(Insumo, RolloInventario.uuid_insumo == Insumo.uuid_insumo)
    )

    # =========================
    #  SALIDAS - MERMA
    # =========================
    retazos = (
        db.session.query(RetazoInventario, RolloInventario, Insumo)
        .join(RolloInventario, RetazoInventario.uuid_rollo_origen == RolloInventario.uuid_rollo)
        .join(Insumo, RolloInventario.uuid_insumo == Insumo.uuid_insumo)
    )

    # =========================
    #  FILTROS EN QUERY (ANTES DE EJECUTAR)
    # =========================
    if form.uuid_insumo.data:
        compras = compras.filter(Insumo.uuid_insumo == form.uuid_insumo.data)
        cortes = cortes.filter(Insumo.uuid_insumo == form.uuid_insumo.data)
        retazos = retazos.filter(Insumo.uuid_insumo == form.uuid_insumo.data)

    if form.fecha_inicio.data:
        compras = compras.filter(CompraEncabezado.fecha_compra >= form.fecha_inicio.data)
        cortes = cortes.filter(EjecucionCorte.fecha_proceso >= form.fecha_inicio.data)
        retazos = retazos.filter(RetazoInventario.fecha_creacion >= form.fecha_inicio.data)

    if form.fecha_fin.data:
        compras = compras.filter(CompraEncabezado.fecha_compra <= form.fecha_fin.data)
        cortes = cortes.filter(EjecucionCorte.fecha_proceso <= form.fecha_fin.data)
        retazos = retazos.filter(RetazoInventario.fecha_creacion <= form.fecha_fin.data)

    # =========================
    #  PROCESAR ENTRADAS
    # =========================
    for detalle, encabezado, insumo in compras.all():

        cantidad = float(detalle.cantidad_comprada * insumo.contenido_cantidad)

        movimientos.append({
            "tipo": "ENTRADA",
            "subtipo": "COMPRA",
            "insumo": insumo.nombre,
            "sku": insumo.sku,
            "cantidad": cantidad,
            "unidad": insumo.contenido_unidad_medida,
            "fecha": encabezado.fecha_compra,
            "referencia": encabezado.uuid_compra,
            "detalle_id": detalle.uuid_detalle_compra
        })

    # =========================
    # 📦 PROCESAR SALIDAS (CONSUMO)
    # =========================
    for corte, rollo, insumo in cortes.all():

        movimientos.append({
            "tipo": "SALIDA",
            "subtipo": "CONSUMO",
            "insumo": insumo.nombre,
            "sku": insumo.sku,
            "cantidad": float(corte.metros_sacados_bodega) * -1,
            "unidad": insumo.contenido_unidad_medida,
            "fecha": corte.fecha_proceso,
            "referencia": corte.uuid_corte,
            "detalle_id": corte.uuid_corte
        })

    # =========================
    # 📦 PROCESAR SALIDAS (MERMA)
    # =========================
    for retazo, rollo, insumo in retazos.all():

        movimientos.append({
            "tipo": "SALIDA",
            "subtipo": "MERMA",
            "insumo": insumo.nombre,
            "sku": insumo.sku,
            "cantidad": float(retazo.metraje) * -1,
            "unidad": insumo.contenido_unidad_medida,
            "fecha": retazo.fecha_creacion,
            "referencia": retazo.uuid_retazo,
            "detalle_id": retazo.uuid_retazo
        })

    # =========================
    # 🔍 FILTROS EN MEMORIA (tipo y subtipo)
    # =========================
    if form.tipo_movimiento.data:
        movimientos = [
            m for m in movimientos
            if m["tipo"] == form.tipo_movimiento.data
        ]

    if form.subtipo.data:
        movimientos = [
            m for m in movimientos
            if m["subtipo"] == form.subtipo.data
        ]

    # =========================
    # 🔄 ORDEN FINAL
    # =========================
    movimientos.sort(key=lambda x: x["fecha"], reverse=True)

    return render_template(
        "produccion/inventario/index.html",
        movimientos=movimientos,
        form=form
    )
'''
@inventario_bp.route("/ver/<uuid_insumo>")
def ver(uuid_insumo):

    insumo = Insumo.query.get_or_404(uuid_insumo)

    rollos = RolloInventario.query.filter_by(
        uuid_insumo=uuid_insumo
    ).all()

    total_rollos = len(rollos)

    total_metros = sum([
        float(r.metraje_continuo_actual or 0)
        for r in rollos
    ])

    return render_template(
        "produccion/inventario/ver.html",
        insumo=insumo,
        rollos=rollos,
        total_rollos=total_rollos,
        total_metros=round(total_metros, 2)
    )