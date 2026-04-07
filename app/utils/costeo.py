from app.models.compras import CompraDetalle, CompraEncabezado
from app.models.insumos import Insumo
from sqlalchemy import desc
from decimal import Decimal

def get_average_cost(uuid_insumo):
    """
    Calcula el costo promedio de las últimas 5 compras recibidas.
    Formula: suma(cantidad * costo) / suma(cantidad)
    """
    recent_purchases = (
        CompraDetalle.query
        .join(CompraEncabezado)
        .filter(
            CompraDetalle.uuid_insumo == uuid_insumo,
            CompraEncabezado.estatus == 'RECIBIDO'
        )
        .order_by(desc(CompraEncabezado.fecha_compra))
        .limit(5)
        .all()
    )

    if not recent_purchases:
        return Decimal('0.00')

    total_cost = Decimal('0.00')
    total_quantity = Decimal('0.00')

    for purchase in recent_purchases:
        qty = Decimal(str(purchase.cantidad_comprada))
        cost = Decimal(str(purchase.costo_unitario_compra))
        total_cost += qty * cost
        total_quantity += qty

    if total_quantity == 0:
        return Decimal('0.00')

    return (total_cost / total_quantity).quantize(Decimal('0.01'))

def get_real_consumption(consumo_teorico, merma_pct):
    """
    Calcula el consumo real ajustado por merma.
    Formula: consumo_real = consumo_teorico * (1 + merma)
    merma_pct es el porcentaje (ej: 0.05 para 5%)
    """
    return Decimal(str(consumo_teorico)) * (Decimal('1.0') + Decimal(str(merma_pct)))

def calculate_utility(precio_actual, costo_mp):
    """
    Utilidad %: ((precio - costo) / costo) * 100
    """
    if not costo_mp or costo_mp == 0:
        return Decimal('0.00')
    
    precio = Decimal(str(precio_actual))
    costo = Decimal(str(costo_mp))
    
    return ((precio - costo) / costo) * Decimal('100.0')

def calculate_adjusted_price(costo_mp, margen_pct):
    """
    Precio Ajustado: costo * (1 + (margen / 100))
    """
    costo = Decimal(str(costo_mp))
    margen = Decimal(str(margen_pct)) / Decimal('100.0')
    
    return costo * (Decimal('1.0') + margen)
