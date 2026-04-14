import os
import uuid
from werkzeug.utils import secure_filename
from . import categorias_bp
from flask_security import login_required, roles_required, hash_password,roles_accepted
from app.models.categorias import Categoria
from app.models.insumos import Insumo
from app.models.proveedores import Proveedor
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from .forms import CategoriaForm
from app.utils.database_connection import db
from flask import render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import or_, func


def _categoria_usos(uuid_categoria):
    """Lista de áreas donde la categoría está referenciada (no vacía si hay uso)."""
    usos = []
    if Insumo.query.filter_by(uuid_categoria=uuid_categoria).first():
        usos.append("insumos")
    if ExplosionMaterialesCabecera.query.filter_by(uuid_categoria=uuid_categoria).first():
        usos.append("recetas / explosión de materiales")
    return usos


def get_upload_folder():
    """Garantiza la existencia y retorna la ruta local de las fotos de categorías."""
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'categorias')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder


@categorias_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente')
def index():
    busqueda = request.args.get("q")
    estatus = request.args.get("estatus")
    query = Categoria.query

    if not estatus or estatus.lower() == "activas":
        query = query.filter(Categoria.estatus_visible == True)
    elif estatus.lower() == "inactivas":
        query = query.filter(Categoria.estatus_visible == False)

    if busqueda:
        busqueda_like = f"%{busqueda.lower()}%"
        query = query.filter(
            or_(
                func.lower(Categoria.nombre).like(busqueda_like),
                func.lower(Categoria.descripcion).like(busqueda_like)
            )
        )

    total_global = Categoria.query.count()
    activas_global = Categoria.query.filter_by(estatus_visible=True).count()
    categorias = query.order_by(Categoria.nombre).all()
    return render_template("produccion/categorias/index.html", categorias=categorias, total_global=total_global, activas_global=activas_global, estatus_actual=estatus)


#  CREAR CATEGORÍA
@categorias_bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente')
def create():
    form = CategoriaForm()

    if form.validate_on_submit():
        # Verificar si ya existe una categoría con el mismo nombre (ignorando mayúsculas/minúsculas)
        nombre_lower = form.nombre.data.strip().lower()
        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre_lower,
            Categoria.tipo == form.tipo.data,
        ).first()

        if categoria_existente:
            flash(f'Ya existe una categoría "{form.nombre.data}" con el mismo tipo.', "error")
            return render_template("produccion/categorias/create.html", form=form, title="Registrar Categoría")

        # Procesar imagen
        imagen_url = "/static/images/default/default-image.png"
        if form.imagen.data:
            file = form.imagen.data
            if file.filename:
                filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
                filepath = os.path.join(get_upload_folder(), filename)
                file.save(filepath)
                imagen_url = f"/static/uploads/categorias/{filename}"

        # Crear nueva categoría con estatus_visible = True siempre
        nueva_categoria = Categoria(
            nombre=form.nombre.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            tipo=form.tipo.data,
            imagen_url=imagen_url,
            estatus_visible=True
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        flash("Categoría creada correctamente", "success")
        return redirect(url_for("categorias_bp.index"))

    return render_template("produccion/categorias/create.html", form=form, title="Registrar Categoría")


#  EDITAR CATEGORÍA
@categorias_bp.route("/edit/<uuid_categoria>", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente')
def edit(uuid_categoria):
    categoria = Categoria.query.get_or_404(uuid_categoria)
    form = CategoriaForm(obj=categoria)
    _t = categoria.tipo
    form.tipo.data = str(getattr(_t, "value", _t)) if _t is not None else "Insumo"

    if form.validate_on_submit():
        nombre_lower = form.nombre.data.strip().lower()
        # Verificar si existe otra categoría con el mismo nombre
        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre_lower,
            Categoria.tipo == form.tipo.data,
            Categoria.uuid_categoria != uuid_categoria,
        ).first()

        if categoria_existente:
            flash(f'Ya existe una categoría "{form.nombre.data}" con el mismo tipo.', "error")
            return render_template("produccion/categorias/edit.html", form=form, title="Editar Categoría", categoria=categoria)

        # Actualizar datos
        categoria.nombre = form.nombre.data.strip()
        categoria.descripcion = form.descripcion.data.strip() if form.descripcion.data else None
        categoria.tipo = form.tipo.data
        categoria.estatus_visible = True

        # Procesar imagen nueva si se proporciona
        if form.imagen.data:
            file = form.imagen.data
            if file.filename:
                filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
                filepath = os.path.join(get_upload_folder(), filename)
                file.save(filepath)
                categoria.imagen_url = f"/static/uploads/categorias/{filename}"

        db.session.commit()
        flash("Categoría actualizada correctamente", "success")
        return redirect(url_for("categorias_bp.index"))

    return render_template("produccion/categorias/edit.html", form=form, title="Editar Categoría", categoria=categoria)


#  DESACTIVAR / ACTIVAR CATEGORÍA
@categorias_bp.route("/delete/<uuid_categoria>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente')
def delete(uuid_categoria):
    categoria = Categoria.query.get_or_404(uuid_categoria)

    # Solo impedir la "baja" (desactivar) si sigue referenciada
    if categoria.estatus_visible:
        usos = _categoria_usos(uuid_categoria)
        if usos:
            flash(
                "No se puede desactivar esta categoría porque está en uso: "
                + ", ".join(usos)
                + ".",
                "error",
            )
            return redirect(url_for("categorias_bp.index"))

    categoria.estatus_visible = not categoria.estatus_visible
    db.session.commit()

    estado = "activada" if categoria.estatus_visible else "desactivada"
    flash(f"Categoría {estado} correctamente", "success")
    return redirect(url_for("categorias_bp.index"))