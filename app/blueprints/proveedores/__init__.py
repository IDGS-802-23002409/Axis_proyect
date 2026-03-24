from flask import Blueprint

proveedores_bp = Blueprint(
    'proveedores', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)
# Inicialización del blueprint
from . import routes 