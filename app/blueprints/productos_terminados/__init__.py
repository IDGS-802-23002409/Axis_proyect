
from flask import Blueprint

productos_bp= Blueprint(
    "productos_bp",
    __name__,
    url_prefix="/productos_terminados"
)

from . import routes