from . import modelos_bp
from flask_security import login_required, roles_accepted
from flask import render_template, redirect, url_for, flash, request
from app.utils.database_connection import db
from app.models.modelos_productos import ModeloRopa
from .forms import ModeloForm
from app.models.categorias import Categoria
from sqlalchemy import or_


# ── INDEX CON BÚSQUEDA Y CREACIÓN DE MODELOS ──────────────────────────────
@modelos_bp.route('/', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'produccion')
def index():
    
    form = ModeloForm(request.form)
    # ── SOLO ACTIVOS ──
    query = ModeloRopa.query.filter_by(estatus='ACTIVO')

    # ── Construir query base ──
    query = ModeloRopa.query

    # ── Búsqueda por nombre de modelo ──
    search_query = request.args.get('q', '').strip()
    if search_query:
        query = query.filter(
            ModeloRopa.nombre_modelo.ilike(f"%{search_query}%")
        )

    # ── Ejecutar query ──
    modelos = query.order_by(ModeloRopa.fecha_creacion.desc()).all()

    # ── Crear nuevo modelo si se envía formulario ──
    if form.validate_on_submit():
        nuevo_modelo = ModeloRopa(
            nombre_modelo=form.nombre_modelo.data.strip(),
            descripcion=form.descripcion.data.strip(),
            uuid_categoria=form.uuid_categoria.data  # asume que seleccionas categoría del form
        )
        db.session.add(nuevo_modelo)
        db.session.commit()
        flash(f'Modelo "{nuevo_modelo.nombre_modelo}" creado con éxito', 'success')
        return redirect(url_for('modelos_bp.index'))

    return render_template(
        'produccion/modelos/index.html',
        modelos=modelos,
        form=form,
        search_query=search_query
    )


@modelos_bp.route('/create', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'produccion')
def create():
    form = ModeloForm()

    if form.validate_on_submit():
        # Crear nuevo modelo
        nuevo_modelo = ModeloRopa(
            nombre_modelo=form.nombre_modelo.data.strip(),
            descripcion=form.descripcion.data.strip(),
            uuid_categoria=form.uuid_categoria.data
        )
        db.session.add(nuevo_modelo)
        db.session.commit()
        flash(f'Modelo "{nuevo_modelo.nombre_modelo}" creado con éxito', 'success')
        return redirect(url_for('modelos_bp.index'))

    # Mostrar formulario
    return render_template(
        'produccion/modelos/create.html',
        form=form
    )

@modelos_bp.route('/edit/<string:uuid_modelo>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'produccion')
def edit(uuid_modelo):
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)
    form = ModeloForm(obj=modelo)  # ← esto precarga los datos

    if form.validate_on_submit():
        modelo.nombre_modelo = form.nombre_modelo.data.strip()
        modelo.descripcion = form.descripcion.data.strip()
        modelo.uuid_categoria = form.uuid_categoria.data

        db.session.commit()
        flash(f'Modelo "{modelo.nombre_modelo}" actualizado con éxito', 'success')
        return redirect(url_for('modelos_bp.index'))

    return render_template(
        'produccion/modelos/edit.html',
        form=form,
        modelo=modelo
    )
@modelos_bp.route('/delete/<string:uuid_modelo>', methods=['POST'])
@login_required
@roles_accepted('admin', 'produccion')
def delete(uuid_modelo):
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)

    if modelo.estatus == 'INACTIVO':
        flash('El modelo ya está inactivo', 'warning')
        return redirect(url_for('modelos_bp.index'))

    modelo.estatus = 'INACTIVO'
    db.session.commit()

    flash(f'Modelo "{modelo.nombre_modelo}" desactivado correctamente', 'success')
    return redirect(url_for('modelos_bp.index'))
@modelos_bp.route('/trash', methods=['GET'])
@login_required
@roles_accepted('admin', 'produccion')
def trash():
    search_query = request.args.get('q', '').strip()

    query = ModeloRopa.query.filter_by(estatus='INACTIVO')

    if search_query:
        query = query.filter(
            ModeloRopa.nombre_modelo.ilike(f"%{search_query}%")
        )

    modelos = query.order_by(ModeloRopa.fecha_actualizacion.desc()).all()

    return render_template(
        'produccion/modelos/trash.html',
        modelos=modelos,
        search_query=search_query
    )

@modelos_bp.route('/restore/<string:uuid_modelo>', methods=['POST'])
@login_required
@roles_accepted('admin', 'produccion')
def restore(uuid_modelo):
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)

    modelo.estatus = 'ACTIVO'
    db.session.commit()

    flash(f'Modelo "{modelo.nombre_modelo}" restaurado correctamente', 'success')
    return redirect(url_for('modelos_bp.trash'))