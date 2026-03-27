from flask import Blueprint

productos_bp = Blueprint('productos', __name__, template_folder='templates/produccion/productos_terminados')

from . import routes
