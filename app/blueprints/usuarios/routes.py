from flask import redirect, render_template, request, url_for
from app.blueprints.usuarios import usuarios_bp
from app.blueprints.usuarios.form import UserForm
from app.models.usuarios import Usuario
from werkzeug.security import generate_password_hash
from app.utils.database_connection import db

@usuarios_bp.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template("usuarios/index.html", usuarios=usuarios)


@usuarios_bp.route("/usuario/registro", methods=["GET", "POST"])
def registroUser():
    form = UserForm(request.form)

    if request.method == "POST" and form.validate():
        user = Usuario(
            nombre_completo=form.nombre_completo.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            rol=form.rol.data,
            estatus=form.estatus.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('usuarios.index'))
    return render_template("usuarios/registro_usuario.html", form=form)
