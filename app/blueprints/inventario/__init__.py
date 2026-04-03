from flask import Blueprint

inventario_bp = Blueprint(
    "inventario_bp",
    __name__,
    url_prefix="/inventario"
)

from . import routes