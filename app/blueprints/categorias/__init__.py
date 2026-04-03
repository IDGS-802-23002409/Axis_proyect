from flask import Blueprint

categorias_bp = Blueprint(
    "categorias_bp",
    __name__,
    url_prefix="/categorias"
)

from . import routes