from flask import render_template
from app.blueprints.usuarios import usuarios_bp
from app.models.usuarios import Usuario

@usuarios_bp.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios)