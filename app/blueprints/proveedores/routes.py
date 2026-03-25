from flask import render_template, redirect, url_for, flash, request
from . import proveedores_bp
from .forms import ProveedorForm
from app.models.proveedores import Proveedor
from app.utils.database_connection import db 
import uuid

# --- CONSULTAR (LISTADO PRINCIPAL) ---
@proveedores_bp.route('/')
def index():
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    form = ProveedorForm()
    
    return render_template('proveedores/index.html', proveedores=all_proveedores, form=form)

# --- CREAR Y ACTUALIZAR ---
@proveedores_bp.route('/guardar', methods=['POST'])
@proveedores_bp.route('/editar/<string:uid>', methods=['POST'])
def guardar(uid=None):
    form = ProveedorForm()
     
    if form.validate_on_submit():
        if uid:
            proveedor = Proveedor.query.get_or_404(uid)
            msg = 'Proveedor actualizado con éxito'
        else:
            proveedor = Proveedor(uuid_proveedor=str(uuid.uuid4()))
            db.session.add(proveedor) 
            msg = 'Proveedor registrado con éxito'

        try:
            proveedor.razon_social = form.razon_social.data
            proveedor.rfc = form.rfc.data
            proveedor.contacto_nombre = form.contacto_nombre.data

            db.session.commit() 
            flash(msg, 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la solicitud: {str(e)}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en {getattr(form, field).label.text}: {error}", 'error')

    return redirect(url_for('proveedores.index'))

# --- ELIMINAR ---
@proveedores_bp.route('/eliminar/<string:uid>', methods=['POST'])
def eliminar(uid):
    try:
        proveedor = Proveedor.query.get_or_404(uid)
        db.session.delete(proveedor)
        db.session.commit()
        flash('Proveedor eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('No se pudo eliminar el proveedor', 'error')
        
    return redirect(url_for('proveedores.index'))