
from flask import Blueprint

orden_bp= Blueprint(
    "orden_bp",
    __name__,
    url_prefix="/orden_produccion"
)

from . import routes