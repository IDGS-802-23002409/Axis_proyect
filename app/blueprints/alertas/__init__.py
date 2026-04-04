from flask import Blueprint

alertas_bp = Blueprint('alertas', __name__, url_prefix='/alertas', template_folder='templates')

from . import routes