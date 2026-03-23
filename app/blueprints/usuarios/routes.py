from flask import render_template
from app.blueprints.usuarios import usuarios_bp
from app.models.usuarios import Usuario

@usuarios_bp.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios)

@usuarios_bp.route('/usuario/registro',methods=[ 'POST'])
def registroUser():
    
    return render_template('usuarios/registro_usuario.html')