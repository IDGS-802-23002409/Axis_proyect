from flask import Blueprint

merma_bp = Blueprint('merma', __name__, url_prefix='/merma')

from . import routes
