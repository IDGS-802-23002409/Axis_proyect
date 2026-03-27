from flask import render_template
from . import alertas_bp
from app.models.modelos_productos import ProductoTerminado
from app.models.insumos import Insumo
from app.models.proveedores import Proveedor

@alertas_bp.route('/')
def index():
    # 1. Detectar niveles (Criterio de Aceptación 1)
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

    # 2. Consolidado para la tabla (Criterio de Aceptación 4: Registro)
    alertas_criticas = []
    for ins in insumos_agotados + insumos_bajo_stock:
        alertas_criticas.append({
            'sku': ins.sku,
            'nombre': ins.nombre,
            'stock': ins.stock_total_acumulado,
            'minimo': ins.stock_minimo_alerta,
            'estado': 'AGOTADO' if ins.stock_total_acumulado == 0 else 'BAJO STOCK'
        })

    return render_template('alertas/index.html', 
                           p_agotadas=len(prendas_agotadas),
                           p_bajo=len(prendas_bajo_stock),
                           i_agotados=len(insumos_agotados),
                           i_bajo=len(insumos_bajo_stock),
                           criticos=alertas_criticas)