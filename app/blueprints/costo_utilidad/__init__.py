from flask import Blueprint

costo_utilidad_bp = Blueprint('costo_utilidad', __name__, template_folder='templates/produccion/costo_utilidad')

from . import routes
