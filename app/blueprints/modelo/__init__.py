from flask import Blueprint

modelo_aux_bp = Blueprint(
    "modelo_aux_bp",
    __name__,
    url_prefix="/recetas_modelo"
)

from . import routes