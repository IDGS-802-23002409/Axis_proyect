from flask import Blueprint

modelos_bp = Blueprint(
    "modelos_bp",
    __name__,
    url_prefix="/recetas"
)

from . import routes