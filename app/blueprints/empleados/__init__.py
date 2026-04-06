from flask import Blueprint

empleados_bp = Blueprint('empleados', __name__)

from app.blueprints.empleados import routes
