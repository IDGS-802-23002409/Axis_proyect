from flask import Blueprint

security_bp = Blueprint('security_bp', __name__, template_folder='../../templates/security')

from . import routes
