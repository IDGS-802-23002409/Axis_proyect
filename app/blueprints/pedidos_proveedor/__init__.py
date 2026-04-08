from flask import Blueprint

pedidos_proveedor_bp = Blueprint(
    'pedidos_proveedor_bp',
    __name__,
    template_folder='../../templates/produccion/pedidos_proveedor'
)

from . import routes
