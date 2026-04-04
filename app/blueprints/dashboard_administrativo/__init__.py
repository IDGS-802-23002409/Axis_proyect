from flask import Blueprint
import os

dashboard_bp = Blueprint(
    'dashboard_administrativo',
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)
from . import routes