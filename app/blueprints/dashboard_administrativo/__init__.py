from flask import Blueprint

dashboard_bp = Blueprint('dashboard_administrativo', __name__, template_folder='templates')

from . import routes