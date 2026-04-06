from flask import Blueprint

modelos_bp = Blueprint('modelos', __name__)

from app.blueprints.modelos import routes
