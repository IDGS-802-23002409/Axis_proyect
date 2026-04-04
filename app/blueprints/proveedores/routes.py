from flask import render_template, redirect, url_for, flash, request, jsonify
from . import proveedores_bp
from .forms import ProveedorForm
from app.models.proveedores import Proveedor
from app.models.usuarios import Usuario
from app.utils.database_connection import db 
from flask_security import login_required, roles_accepted, roles_required, current_user
import uuid
import re


# --- CONSULTAR (LISTADO PRINCIPAL) ---
@proveedores_bp.route('/')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    form = ProveedorForm()
    return render_template('index.html', proveedores=all_proveedores, form=form,
                           top_producto={'nombre': 'Shadow Hoodie', 'unidades': 42, 'monto': 12500.50, 'imagen': None},
                           bottom_producto={'nombre': 'Basic Tee White', 'stock': 85, 'imagen': None})

# --- CREAR Y ACTUALIZAR ---
@proveedores_bp.route('/guardar', methods=['POST'])
@proveedores_bp.route('/editar/<string:uid>', methods=['POST'])
@login_required
@roles_accepted('admin', 'gerente')
def guardar(uid=None):
    form = ProveedorForm()
    
    if form.validate_on_submit():
        if uid:
            proveedor = Proveedor.query.get_or_404(uid)
            msg = 'Proveedor actualizado con éxito'
        else:
            proveedor = Proveedor(uuid_proveedor=str(uuid.uuid4()))
            proveedor.usuario_creo_uuid = current_user.uuid_usuario
            db.session.add(proveedor) 
            msg = 'Proveedor registrado con éxito'

        try:
            proveedor.razon_social = form.razon_social.data.upper()
            proveedor.rfc = form.rfc.data.upper() if form.rfc.data else ""
            proveedor.contacto_nombre = form.contacto_nombre.data
            
            if form.telefono.data:
                proveedor.telefono = re.sub(r'\D', '', form.telefono.data)     
            
            proveedor.categoria_insumo = form.categoria_insumo.data
            
            if uid:
                proveedor.estatus = form.estatus.data

            db.session.commit()
            flash(msg, 'success')
            return redirect(url_for('proveedores.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}', 'error')
            return redirect(url_for('proveedores.index'))
    
    # Si falla la validación, recarga los errores
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    target_modal = 'modal-update' if uid else 'modal-registro'
    return render_template('index.html', proveedores=all_proveedores, form=form, modal_to_open=target_modal,
                           edit_uid=uid)

# --- ELIMINAR ---
@proveedores_bp.route('/eliminar/<string:uid>', methods=['POST'])
@login_required
@roles_required('admin') # Solo el admin puede borrar
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

@proveedores_bp.route('/<string:uid>')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def detalles(uid):
    p = Proveedor.query.get_or_404(uid)
    
    # --- LOGICA DE REDIRECCIÓN ---
    # Si NO viene el parámetro format=json, significa que el usuario entró desde la URL
    if request.args.get('format') != 'json':
        proveedores = Proveedor.query.all()
        from .forms import ProveedorForm # Asegúrate de que el nombre sea correcto
        form = ProveedorForm()
        
        return render_template('index.html', proveedores=proveedores, form=form)

    uuid_a_mostrar = p.usuario_creo_uuid if p.usuario_creo_uuid else "SISTEMA"
    return jsonify({
        "uuid": str(p.uuid_proveedor), 
        "razon_social": p.razon_social,
        "rfc": p.rfc,
        "contacto_nombre": p.contacto_nombre,
        "telefono": p.telefono,           
        "categoria_insumo": p.categoria_insumo, 
        "estatus": bool(p.estatus),
        "fecha_creacion": p.fecha_creacion.strftime('%d/%m/%Y %H:%M') if p.fecha_creacion else '---',
        "fecha_actualizacion": p.fecha_actualizacion.strftime('%d/%m/%Y %H:%M') if p.fecha_actualizacion else '---',
        "usuario_creo": uuid_a_mostrar
    })