from flask import flash, redirect, render_template, request, url_for
from app.blueprints.productos_terminados import productos_bp
from app.blueprints.productos_terminados.form import ProductoTerminadoForm
from app.models.modelos_productos import ProductoTerminado, ModeloRopa
from app.utils.database_connection import db

@productos_bp.route('/')
def index():

    return render_template(
        'produccion/productos_terminados/index.html',

    )
