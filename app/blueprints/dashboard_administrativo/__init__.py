from flask import Blueprint

dashboard_bp = Blueprint('dashboard_admnistrativo', __name__, template_folder='templates')

from . import routes