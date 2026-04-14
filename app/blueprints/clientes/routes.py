from flask import flash, redirect, render_template, request, url_for
import re
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
        
    clientes = clientes.filter(Usuario.active == True).all()
    total_clientes = len(clientes)

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
            telefono=re.sub(r'\D', '', str(form.telefono.data)),
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
            cli.telefono = re.sub(r'\D', '', str(form.telefono.data))
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

    from app.models.ventas import VentaEncabezado
    pedidos_pendientes = VentaEncabezado.query.filter_by(uuid_cliente=cli.uuid_cliente).filter(VentaEncabezado.estatus_envio.in_(['Procesando', 'Pendiente'])).count()
    if pedidos_pendientes > 0:
         flash("No se puede desactivar el perfil del cliente porque tiene pedidos en curso.", "error")
         return redirect(url_for('clientes.index'))

    cli.usuario.active = False
    db.session.commit()
    flash("Perfil de cliente desactivado", "success")
    return redirect(url_for('clientes.index'))

@clientes_bp.route("/ver/<uuid_cliente>")
@login_required
def view_cliente(uuid_cliente):
    cli = Cliente.query.get_or_404(uuid_cliente)
    return render_template("produccion/clientes/ver.html", cliente=cli)

@clientes_bp.route("/inactivos")
@login_required
@roles_accepted('admin', 'gerente')
def trash():
    clientes = Cliente.query.join(Usuario).filter(Usuario.active == False).all()
    return render_template("produccion/clientes/trash.html", clientes=clientes)

@clientes_bp.route("/restore/<uuid_cliente>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente')
def restore(uuid_cliente):
    cli = Cliente.query.get_or_404(uuid_cliente)
    cli.usuario.active = True
    db.session.commit()
    flash("Perfil de cliente reactivado", "success")
    return redirect(url_for('clientes.trash'))

