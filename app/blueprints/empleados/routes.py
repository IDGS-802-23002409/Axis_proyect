from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required, roles_accepted
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
    empleados = Empleado.query.join(Usuario)
    if q:
        empleados = empleados.filter(Usuario.nombre_completo.ilike(f"%{q}%"))
        
    empleados = empleados.all()
    total_empleados = Empleado.query.count()

    return render_template(
        "produccion/empleados/index.html",
        empleados=empleados,
        total_empleados=total_empleados,
        q=q
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
            fecha_ingreso=form.fecha_ingreso.data
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
    empelado = Empleado.query.get_or_404(uuid_empleado)

    if request.method == "POST":
        form = EmpleadoForm(request.form, obj=empelado)
        if form.validate():
            empelado.uuid_usuario = form.uuid_usuario.data
            empelado.numero_empleado = form.numero_empleado.data
            empelado.puesto = form.puesto.data
            empelado.departamento = form.departamento.data
            empelado.fecha_ingreso = form.fecha_ingreso.data
            
            db.session.commit()
            flash("Empleado actualizado correctamente", "success")
            return redirect(url_for('empleados.index'))
    else:
        form = EmpleadoForm(obj=empelado)

    return render_template("produccion/empleados/update_empleado.html", form=form, empleado=empelado)

@empleados_bp.route("/eliminar/<uuid_empleado>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente')
def delete_empleado(uuid_empleado):
    empelado = Empleado.query.get_or_404(uuid_empleado)
    db.session.delete(empelado)
    db.session.commit()
    flash("Perfil de empleado eliminado correctamente", "success")
    return redirect(url_for('empleados.index'))
