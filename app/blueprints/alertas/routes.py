from flask import render_template
from . import alertas_bp
from app.models.modelos_productos import ProductoTerminado
from app.models.insumos import Insumo
from app.models.proveedores import Proveedor
from app.models.compras import CompraEncabezado, CompraDetalle


@alertas_bp.route('/')
def index():
    # 1. Detectar niveles críticos
    prendas_agotadas = ProductoTerminado.query.filter_by(stock_fisico_actual=0).all()
    prendas_bajo_stock = ProductoTerminado.query.filter(
        ProductoTerminado.stock_fisico_actual > 0,
        ProductoTerminado.stock_fisico_actual <= ProductoTerminado.stock_minimo_alerta
    ).all()

    insumos_agotados = Insumo.query.filter_by(stock_total_acumulado=0).all()
    insumos_bajo_stock = Insumo.query.filter(
        Insumo.stock_total_acumulado > 0,
        Insumo.stock_total_acumulado <= Insumo.stock_minimo_alerta
    ).all()

    criticos = []
    for ins in insumos_agotados + insumos_bajo_stock:
        # Buscar proveedor por categoría del insumo
        proveedor = None
        # Buscar último proveedor por historial de compras
        last_compra = (
            CompraDetalle.query.filter_by(uuid_insumo=ins.uuid_insumo)
            .join(CompraEncabezado)
            .order_by(CompraEncabezado.fecha_compra.desc())
            .first()
        )
        proveedor = last_compra.compra.proveedor if last_compra else None

        criticos.append({
            'uuid_insumo'       : ins.uuid_insumo,
            'sku'               : ins.sku or '—',
            'nombre'            : ins.nombre,
            'stock'             : float(ins.stock_total_acumulado),
            'minimo'            : float(ins.stock_minimo_alerta),
            'estado'            : 'AGOTADO' if ins.stock_total_acumulado == 0 else 'BAJO STOCK',
            # Datos del proveedor para el modal
            'proveedor_nombre'  : proveedor.razon_social if proveedor else '—',
            'proveedor_rfc'     : proveedor.rfc if proveedor else '—',
            'proveedor_tel'     : proveedor.telefono if proveedor else '—',
            'proveedor_contacto': proveedor.contacto_nombre if proveedor else '—',
            'proveedor_uuid'    : proveedor.uuid_proveedor if proveedor else None,
        })

    return render_template(
        'alertas/index.html',
        p_agotadas = len(prendas_agotadas),
        p_bajo     = len(prendas_bajo_stock),
        i_agotados = len(insumos_agotados),
        i_bajo     = len(insumos_bajo_stock),
        criticos   = criticos,
    )