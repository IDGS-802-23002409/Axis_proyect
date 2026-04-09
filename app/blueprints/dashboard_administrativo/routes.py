from flask import render_template, flash, request
from flask_security import login_required, roles_accepted
from . import dashboard_bp
from app.utils.database_connection import db
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.insumos import Insumo
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from calendar import monthrange


def _ventas_por_dia(year: int, month: int) -> dict:
    """Devuelve {dia: monto} para todos los días del mes indicado."""
    rows = (
        db.session.query(
            extract('day', VentaEncabezado.fecha_venta).label('dia'),
            func.sum(
                VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico
            ).label('monto'),
        )
        .join(VentaDetalle, VentaEncabezado.uuid_venta == VentaDetalle.uuid_venta)
        .filter(
            extract('year',  VentaEncabezado.fecha_venta) == year,
            extract('month', VentaEncabezado.fecha_venta) == month,
        )
        .group_by('dia')
        .all()
    )
    return {int(r.dia): float(r.monto) for r in rows}


def _top_bottom_productos(fecha_inicio, fecha_fin):
    """
    Devuelve (top_unidades, top_monto, bottom_unidades, bottom_monto)
    para el rango dado.
    """
    base = (
        db.session.query(
            ExplosionMaterialesCabecera.nombre_receta,
            ExplosionMaterialesCabecera.talla,
            func.coalesce(func.sum(VentaDetalle.cantidad), 0).label('total_u'),
            func.coalesce(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico), 0
            ).label('total_m'),
        )
        .select_from(ProductoTerminado)
        .join(ExplosionMaterialesCabecera, ProductoTerminado.uuid_explosion == ExplosionMaterialesCabecera.uuid_explosion)
        .outerjoin(VentaDetalle,    ProductoTerminado.uuid_producto == VentaDetalle.uuid_producto)
        .outerjoin(VentaEncabezado, VentaDetalle.uuid_venta == VentaEncabezado.uuid_venta)
        .filter(
            (func.date(VentaEncabezado.fecha_venta).between(fecha_inicio, fecha_fin)) |
            (VentaEncabezado.fecha_venta == None)
        )
        .group_by(ExplosionMaterialesCabecera.nombre_receta, ExplosionMaterialesCabecera.talla)
        .all()
    )

    if not base:
        return None, None, None, None

    by_u = sorted(base, key=lambda r: r.total_u, reverse=True)
    by_m = sorted(base, key=lambda r: r.total_m, reverse=True)

    def _fmt(r, key):
        return {
            'nombre'  : f"{r.nombre_receta} · {r.talla}",
            'unidades': int(r.total_u),
            'monto'   : float(r.total_m),
            'imagen'  : None,
        }

    return (
        _fmt(by_u[0],  'u'),   # top por unidades
        _fmt(by_m[0],  'm'),   # top por monto
        _fmt(by_u[-1], 'u'),   # bottom por unidades
        _fmt(by_m[-1], 'm'),   # bottom por monto
    )


@dashboard_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente')
def index():
    try:
        hoy         = datetime.now().date()
        mes_actual  = hoy.month
        anio_actual = hoy.year

        # Mes anterior
        if mes_actual == 1:
            mes_ant  = 12
            anio_ant = anio_actual - 1
        else:
            mes_ant  = mes_actual - 1
            anio_ant = anio_actual

        # ── KPI: ventas del mes actual (acumulado hasta hoy) ──────────────
        ventas_mes = float(
            db.session.query(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
            ).join(VentaEncabezado)
             .filter(
                 extract('year',  VentaEncabezado.fecha_venta) == anio_actual,
                 extract('month', VentaEncabezado.fecha_venta) == mes_actual,
             ).scalar() or 0
        )

        # KPI: ventas mes anterior (completo)
        ventas_mes_ant = float(
            db.session.query(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
            ).join(VentaEncabezado)
             .filter(
                 extract('year',  VentaEncabezado.fecha_venta) == anio_ant,
                 extract('month', VentaEncabezado.fecha_venta) == mes_ant,
             ).scalar() or 0
        )

        variacion_pct = (
            round(((ventas_mes - ventas_mes_ant) / ventas_mes_ant) * 100, 1)
            if ventas_mes_ant > 0 else (100.0 if ventas_mes > 0 else 0.0)
        )
        tendencia = "up" if variacion_pct >= 0 else "down"

        # ── KPI: ventas de HOY ─────────────────────────────────────────────
        ventas_hoy = float(
            db.session.query(
                func.sum(VentaDetalle.cantidad * VentaDetalle.precio_unitario_historico)
            ).join(VentaEncabezado)
             .filter(func.date(VentaEncabezado.fecha_venta) == hoy)
             .scalar() or 0
        )

        # ── Gráfica: mes actual vs mes anterior día a día ─────────────────
        dias_mes_actual = monthrange(anio_actual, mes_actual)[1]
        dias_mes_ant    = monthrange(anio_ant, mes_ant)[1]
        max_dias        = max(dias_mes_actual, dias_mes_ant)

        datos_actual = _ventas_por_dia(anio_actual, mes_actual)
        datos_ant    = _ventas_por_dia(anio_ant, mes_ant)

        chart_labels   = [str(d) for d in range(1, max_dias + 1)]
        chart_data_act = [datos_actual.get(d, 0) for d in range(1, max_dias + 1)]
        chart_data_ant = [datos_ant.get(d, 0)    for d in range(1, max_dias + 1)]

        # Nombres de meses en español para la leyenda
        MESES = ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        label_actual = f"{MESES[mes_actual]} {anio_actual}"
        label_ant    = f"{MESES[mes_ant]} {anio_ant}"

        # ── Top / Bottom productos (últimos 30 días) ───────────────────────
        hace_30 = hoy - timedelta(days=30)
        top_u, top_m, bot_u, bot_m = _top_bottom_productos(hace_30, hoy)

        return render_template(
            'dashboard/index.html',
            # KPIs
            ventas_hoy       = ventas_hoy,
            ventas_mes       = ventas_mes,
            ventas_mes_ant   = ventas_mes_ant,
            variacion_pct    = variacion_pct,
            tendencia        = tendencia,
            label_actual     = label_actual,
            label_ant        = label_ant,
            # Cards productos
            top_u            = top_u,
            top_m            = top_m,
            bot_u            = bot_u,
            bot_m            = bot_m,
            # Gráfica
            chart_labels     = chart_labels,
            chart_data_act   = chart_data_act,
            chart_data_ant   = chart_data_ant,
        )

    except Exception as e:
        db.session.rollback()
        flash(f"Error interno: {str(e)}", "danger")
        return render_template(
            'dashboard/index.html',
            ventas_hoy=0, ventas_mes=0, ventas_mes_ant=0,
            variacion_pct=0, tendencia='up',
            label_actual='', label_ant='',
            top_u=None, top_m=None, bot_u=None, bot_m=None,
            chart_labels=[], chart_data_act=[], chart_data_ant=[],
        )