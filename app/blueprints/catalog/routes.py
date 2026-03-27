from flask import Blueprint, render_template

catalog_bp = Blueprint('catalog', __name__, template_folder='../../templates/client')

@catalog_bp.route('/')
def index():
    return render_template('catalog/index.html')

@catalog_bp.route('/catalog')
def catalog_view():
    return render_template('catalog/catalog.html')
