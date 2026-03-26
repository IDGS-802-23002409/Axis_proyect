from flask import render_template, redirect, url_for, flash, request, jsonify
from . import proveedores_bp
from .forms import ProveedorForm
from app.models.proveedores import Proveedor
from app.utils.database_connection import db 
import uuid
from app.app import csrf
import re

# --- CONSULTAR (LISTADO PRINCIPAL) ---
@proveedores_bp.route('/')
def index():
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    form = ProveedorForm()
    
    # Si la petición viene de Postman o JS (Header: Accept: application/json)
    if request.is_json or request.args.get('format') == 'json':
        return jsonify([{
            "uuid": p.uuid_proveedor,
            "razon_social": p.razon_social,
            "rfc": p.rfc,
            "contacto": p.contacto_nombre
        } for p in all_proveedores])

    # Si es el navegador normal
    return render_template('index.html', proveedores=all_proveedores, form=form)

# --- CREAR Y ACTUALIZAR ---
@proveedores_bp.route('/guardar', methods=['POST'])
@proveedores_bp.route('/editar/<string:uid>', methods=['POST'])
@csrf.exempt
def guardar(uid=None):
    form = ProveedorForm()
    is_api_request = request.is_json or request.args.get('format') == 'json'
    
    if form.validate_on_submit() or (is_api_request and form.validate()):
        if uid:
            proveedor = Proveedor.query.get_or_404(uid)
            msg = 'Proveedor actualizado con éxito'
        else:
            proveedor = Proveedor(uuid_proveedor=str(uuid.uuid4()))
            db.session.add(proveedor) 
            msg = 'Proveedor registrado con éxito'

        try:
            if is_api_request and request.json:
                proveedor.razon_social = request.json.get('razon_social')
                proveedor.rfc = request.json.get('rfc')
                proveedor.contacto_nombre = request.json.get('contacto_nombre')
                if 'estatus' in request.json:
                    proveedor.estatus = request.json.get('estatus')
            else:
                proveedor.razon_social = form.razon_social.data
                proveedor.rfc = form.rfc.data
                proveedor.contacto_nombre = form.contacto_nombre.data
                if form.telefono.data:
                    proveedor.telefono = re.sub(r'\D', '', form.telefono.data)     
                proveedor.categoria_insumo = form.categoria_insumo.data
                
                if uid:
                    # form.estatus.data será True si está marcado, False si no
                    proveedor.estatus = form.estatus.data

            db.session.commit()
            
            if is_api_request:
                return jsonify({"status": "success", "message": msg}), 200
            
            flash(msg, 'success')
            return redirect(url_for('proveedores.index'))
            
        except Exception as e:
            db.session.rollback()
            if is_api_request:
                return jsonify({"status": "error", "message": str(e)}), 500
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('proveedores.index'))
    else:
        # Manejo de errores de validación
        if is_api_request:
            return jsonify({"status": "error", "errors": form.errors}), 400
            
        for field, errors in form.errors.items():
           for field, errors in form.errors.items():
             for error in errors:
                 flash(f"{getattr(form, field).label.text}: {error}", "error")
        else:
        # Manejo de errores de validación
         if is_api_request:
            return jsonify({"status": "error", "errors": form.errors}), 400
            
        all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
        
        return render_template('index.html', proveedores=all_proveedores, form=form)

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

@proveedores_bp.route('/<string:uid>')
def detalles(uid):
    p = Proveedor.query.get_or_404(uid)
    return jsonify({
        "uuid": str(p.uuid_proveedor), 
        "razon_social": p.razon_social,
        "rfc": p.rfc,
        "contacto_nombre": p.contacto_nombre,
        "telefono": p.telefono,          
        "categoria_insumo": p.categoria_insumo, 
        "estatus": bool(p.estatus)
    })