from flask import Blueprint

compras_bp = Blueprint(
    "compras_bp",
    __name__,
    url_prefix="/compras"
)

from . import routes