from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func
from app.blueprints.usuarios import usuarios_bp
from app.blueprints.usuarios.form import UserForm
from app.models.usuarios import Usuario, Role,roles_usuarios
from flask_security.utils import hash_password
from app.utils.database_connection import db


@usuarios_bp.route("/")
def index():
    usuarios = Usuario.query.all()
    total_usuarios = Usuario.query.count()
    administradores = (
        db.session.query(func.count(Usuario.uuid_usuario))
        .join(roles_usuarios)
        .join(Role)
        .filter(Role.name == "admin")
        .scalar()
    )

    personal_produccion = (
        db.session.query(func.count(Usuario.uuid_usuario))
        .join(roles_usuarios)
        .join(Role)
        .filter(Role.name == "produccion")
        .scalar()
    )
    inactivos = Usuario.query.filter_by(active=False).count()

    return render_template("produccion/usuarios/index.html", usuarios=usuarios,
                           total_usuarios=total_usuarios,
                            administradores=administradores,
                            personal_produccion=personal_produccion,
                            inactivos=inactivos)

@usuarios_bp.route("/usuario/registro", methods=["GET", "POST"])
def registroUser():
    form = UserForm()
    if request.method == "POST" and form.validate():
        existing_user = Usuario.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("El correo ya está registrado", "error")
            return render_template("usuarios/registro_usuario.html", form=form)

        user = Usuario(
            nombre_completo=form.nombre_completo.data,
            email=form.email.data,
            password=hash_password(form.password.data)
        )

        role = Role.query.filter_by(name=form.rol.data).first()
        if role:
            user.roles.append(role)

        db.session.add(user)
        db.session.commit()
        flash("Usuario creado correctamente", "success")
        return redirect(url_for('usuarios.index'))

    return render_template("produccion/usuarios/registro_usuario.html", form=form)

@usuarios_bp.route("/usuario/editar/<uuid>", methods=["GET", "POST"])
def updateUser(uuid):
    user = Usuario.query.get_or_404(uuid)

    if request.method == "POST":
        form = UserForm(request.form, obj=user)

        if form.validate():

            existing_user = Usuario.query.filter_by(email=form.email.data).first()
            if existing_user and existing_user.uuid_usuario != user.uuid_usuario:
                flash("El correo ya está en uso", "error")
                return render_template("produccion/usuarios/update_user.html", form=form)

            user.nombre_completo = form.nombre_completo.data
            user.email = form.email.data
            user.active = form.active.data

            role = Role.query.filter_by(name=form.rol.data).first()
            if role:
                user.roles = [role]

            if form.password.data:
                user.password = hash_password(form.password.data)

            db.session.commit()

            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for('usuarios.index'))

    else:
        form = UserForm(obj=user)

        if user.roles:
            form.rol.data = user.roles[0].name

    return render_template("produccion/usuarios/update_user.html", form=form)

@usuarios_bp.route("/usuario/eliminar/<uuid>", methods=["POST"])
def deleteUser(uuid):
    user = Usuario.query.get_or_404(uuid)

    if any(role.name == "admin" for role in user.roles):
        flash("No se puede eliminar un administrador", "error")
        return redirect(url_for('usuarios.index'))

    user.active = False
    db.session.commit()

    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for('usuarios.index'))