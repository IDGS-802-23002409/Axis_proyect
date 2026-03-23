from flask import render_template, redirect, url_for, flash, request
from . import proveedores_bp
from .forms import ProveedorForm
from app.models import Proveedor
from app.utils.database_connection import db
import uuid

@proveedores_bp.route('/')
def index():
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    form = ProveedorForm()
    return render_template('proveedores/index.html', proveedores=all_proveedores, form=form)

@proveedores_bp.route('/crear', methods=['POST'])
def crear():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_p = Proveedor(
            uuid_proveedor=str(uuid.uuid4()),
            razon_social=form.razon_social.data,
            rfc=form.rfc.data,
            contacto_nombre=form.contacto_nombre.data,
            # categoria_insumo=form.categoria_insumo.data
        )
        db.session.add(nuevo_p)
        db.session.commit()
        flash('Proveedor registrado con éxito', 'success')
    return redirect(url_for('proveedores.index'))

@proveedores_bp.route('/eliminar/<string:uid>', methods=['POST'])
def eliminar(uid):
    proveedor = Proveedor.query.get_or_404(uid)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado', 'warning')
    return redirect(url_for('proveedores.index'))