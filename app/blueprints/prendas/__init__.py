from flask import Blueprint
import os
prendas_bp = Blueprint(
    'prendas',
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

from . import routes  # noqa: E402, F401