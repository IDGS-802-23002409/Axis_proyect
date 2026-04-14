from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required, roles_accepted, current_user
from app.blueprints.empleados import empleados_bp
from app.blueprints.empleados.form import EmpleadoForm
from app.models.empleados import Empleado
from app.models.usuarios import Usuario
from app.utils.database_connection import db

@empleados_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente')
def index():
    q = request.args.get('q', '').strip()
    estado = request.args.get('estado', 'activos').strip().lower()

    empleados = Empleado.query.join(Usuario)

    if estado == 'inactivos':
        empleados = empleados.filter(Empleado.activo == False)
    else:
        empleados = empleados.filter(Empleado.activo == True)

    if q:
        empleados = empleados.filter(Usuario.nombre_completo.ilike(f"%{q}%"))

    empleados = empleados.all()
    total_empleados = Empleado.query.filter_by(activo=True).count()

    return render_template(
        "produccion/empleados/index.html",
        empleados=empleados,
        total_empleados=total_empleados,
        q=q,
        estado=estado
    )

@empleados_bp.route("/registro", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente')
def registro_empleado():
    form = EmpleadoForm()
    if request.method == "POST" and form.validate():
        nuevo_empleado = Empleado(
            uuid_usuario=form.uuid_usuario.data,
            numero_empleado=form.numero_empleado.data,
            puesto=form.puesto.data,
            departamento=form.departamento.data,
            fecha_ingreso=form.fecha_ingreso.data,
            activo=True
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        flash("Empleado registrado correctamente", "success")
        return redirect(url_for('empleados.index'))

    return render_template("produccion/empleados/registro_empleado.html", form=form)

@empleados_bp.route("/editar/<uuid_empleado>", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente')
def update_empleado(uuid_empleado):
    empleado = Empleado.query.get_or_404(uuid_empleado)

    if request.method == "POST":
        form = EmpleadoForm(request.form, obj=empleado)
        if form.validate():
            empleado.uuid_usuario = form.uuid_usuario.data
            empleado.numero_empleado = form.numero_empleado.data
            empleado.puesto = form.puesto.data
            empleado.departamento = form.departamento.data
            empleado.fecha_ingreso = form.fecha_ingreso.data

            db.session.commit()
            flash("Empleado actualizado correctamente", "success")
            return redirect(url_for('empleados.index'))
    else:
        form = EmpleadoForm(obj=empleado)

    return render_template("produccion/empleados/update_empleado.html", form=form, empleado=empleado)

@empleados_bp.route("/ver/<uuid_empleado>")
@login_required
@roles_accepted('admin', 'gerente')
def ver_empleado(uuid_empleado):
    empleado = Empleado.query.get_or_404(uuid_empleado)
    return render_template("produccion/empleados/ver_empleado.html", empleado=empleado)

@empleados_bp.route("/eliminar/<uuid_empleado>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente')
def delete_empleado(uuid_empleado):
    empleado = Empleado.query.get_or_404(uuid_empleado)

    # Bug 4: Proteger a usuarios con rol "admin"
    usuario = Usuario.query.get(empleado.uuid_usuario)
    if usuario:
        roles = [r.name for r in usuario.roles]
        if 'admin' in roles:
            flash("No se puede desactivar el perfil de un Administrador del sistema.", "error")
            return redirect(url_for('empleados.index'))

    # Bug 5: Borrado lógico
    empleado.activo = False
    db.session.commit()
    flash("Perfil de empleado desactivado correctamente", "success")
    return redirect(url_for('empleados.index'))
