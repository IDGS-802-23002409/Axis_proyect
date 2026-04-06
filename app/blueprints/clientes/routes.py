from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required, roles_required, roles_accepted
from app.blueprints.clientes import clientes_bp
from app.blueprints.clientes.form import ClienteForm
from app.models.clientes import Cliente
from app.models.usuarios import Usuario
from app.utils.database_connection import db

@clientes_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente')
def index():
    q = request.args.get('q', '').strip()
    clientes = Cliente.query.join(Usuario)
    
    if q:
        clientes = clientes.filter(Usuario.nombre_completo.ilike(f"%{q}%"))
        
    clientes = clientes.all()
    total_clientes = Cliente.query.count()

    return render_template(
        "produccion/clientes/index.html",
        clientes=clientes,
        total_clientes=total_clientes,
        q=q
    )

@clientes_bp.route("/registro", methods=["GET", "POST"])
@login_required
def registro_cliente():
    form = ClienteForm()
    if request.method == "POST" and form.validate():
        nuevo_ = Cliente(
            uuid_usuario=form.uuid_usuario.data,
            telefono=form.telefono.data,
            direccion_completa=form.direccion_completa.data
        )
        db.session.add(nuevo_)
        db.session.commit()
        flash("Cliente registrado correctamente", "success")
        return redirect(url_for('clientes.index'))

    return render_template("produccion/clientes/registro_cliente.html", form=form)

@clientes_bp.route("/editar/<uuid_cliente>", methods=["GET", "POST"])
@login_required
def update_cliente(uuid_cliente):
    cli = Cliente.query.get_or_404(uuid_cliente)

    if request.method == "POST":
        form = ClienteForm(request.form, obj=cli)
        if form.validate():
            cli.uuid_usuario = form.uuid_usuario.data
            cli.telefono = form.telefono.data
            cli.direccion_completa = form.direccion_completa.data
            
            db.session.commit()
            flash("Cliente actualizado correctamente", "success")
            return redirect(url_for('clientes.index'))
    else:
        form = ClienteForm(obj=cli)

    return render_template("produccion/clientes/update_cliente.html", form=form, cliente=cli)

@clientes_bp.route("/eliminar/<uuid_cliente>", methods=["POST"])
@login_required
def delete_cliente(uuid_cliente):
    cli = Cliente.query.get_or_404(uuid_cliente)

    db.session.delete(cli)
    db.session.commit()
    flash("Perfil de cliente eliminado", "success")
    return redirect(url_for('clientes.index'))
