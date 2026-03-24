from flask import render_template, redirect, url_for, flash, request, jsonify
from . import proveedores_bp
from .forms import ProveedorForm
from app.models.proveedores import Proveedor
from app.utils.database_connection import db 
import uuid
# Rutas de CREAR, ACTUALIZAR, DETALLES y ELIMINAR de proveedores
# --- CONSULTAR (LISTADO PRINCIPAL) ---
@proveedores_bp.route('/')
def index():
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    
    return jsonify([{
        "uuid": p.uuid_proveedor,
        "razon_social": p.razon_social,
        "rfc": p.rfc,
        "contacto": p.contacto_nombre
    } for p in all_proveedores])

# --- CREAR Y ACTUALIZAR (LÓGICA UNIFICADA) ---
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
           
            msg = 'Proveedor registrado con éxito'

        try:
            # Mapeo de datos
            proveedor.razon_social = form.razon_social.data
            proveedor.rfc = form.rfc.data
            proveedor.contacto_nombre = form.contacto_nombre.data

            db.session.commit() 
            
            return jsonify({"status": "success", "message": msg}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "errors": form.errors}), 400

# --- ELIMINAR ---
@proveedores_bp.route('/eliminar/<string:uid>', methods=['POST'])
def eliminar(uid):
    try:
        proveedor = Proveedor.query.get_or_404(uid)
        db.session.delete(proveedor)
        db.session.commit()
        return jsonify({"status": "success", "message": "Eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "No se pudo eliminar"}), 500

# --- API: OBTENER DATOS (DETALLES) ---
@proveedores_bp.route('/<uid>')
def detalles(uid):
    p = Proveedor.query.get_or_404(uid)
    return jsonify({
        "uuid": p.uuid_proveedor,
        "razon_social": p.razon_social,
        "rfc": p.rfc,
        "contacto_nombre": p.contacto_nombre
    })