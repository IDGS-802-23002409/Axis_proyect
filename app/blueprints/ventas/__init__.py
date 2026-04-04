from flask import Blueprint
import os

ventas_bp = Blueprint(
    'ventas',
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

from . import routes  # noqa