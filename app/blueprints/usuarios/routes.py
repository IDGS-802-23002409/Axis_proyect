from flask import render_template
from usuarios import usuarios_bp

@usuarios_bp.route('/')
def index():
    return render_template('usuarios/index.html')