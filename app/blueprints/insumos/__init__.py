from flask import Blueprint

insumos_bp = Blueprint(
    "insumos_bp",
    __name__,
    url_prefix="/insumos"
)

from . import routes