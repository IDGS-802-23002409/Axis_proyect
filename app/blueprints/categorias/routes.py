from . import categorias_bp
from app.models.categorias import Categoria
from .forms import CategoriaForm
from app.utils.database_connection import db
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_, func


@categorias_bp.route("/")
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

    categorias = query.order_by(Categoria.nombre).all()
    return render_template("produccion/categorias/index.html", categorias=categorias)


# 🔹 CREAR CATEGORÍA
@categorias_bp.route("/create", methods=["GET", "POST"])
def create():
    form = CategoriaForm()

    if form.validate_on_submit():
        # Verificar si ya existe una categoría con el mismo nombre (ignorando mayúsculas/minúsculas)
        nombre_lower = form.nombre.data.strip().lower()
        categoria_existente = Categoria.query.filter(db.func.lower(Categoria.nombre) == nombre_lower).first()

        if categoria_existente:
            flash(f'La categoría "{form.nombre.data}" ya existe.', "error")
            return render_template("produccion/categorias/create.html", form=form, title="Registrar Categoría")

        # Crear nueva categoría con estatus_visible = True siempre
        nueva_categoria = Categoria(
            nombre=form.nombre.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            estatus_visible=True
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        flash("Categoría creada correctamente", "success")
        return redirect(url_for("categorias_bp.index"))

    return render_template("produccion/categorias/create.html", form=form, title="Registrar Categoría")


# 🔹 EDITAR CATEGORÍA
@categorias_bp.route("/edit/<uuid_categoria>", methods=["GET", "POST"])
def edit(uuid_categoria):
    categoria = Categoria.query.get_or_404(uuid_categoria)
    form = CategoriaForm(obj=categoria)

    if form.validate_on_submit():
        nombre_lower = form.nombre.data.strip().lower()
        # Verificar si existe otra categoría con el mismo nombre
        categoria_existente = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre_lower,
            Categoria.uuid_categoria != uuid_categoria
        ).first()

        if categoria_existente:
            flash(f'La categoría "{form.nombre.data}" ya existe.', "error")
            return render_template("produccion/categorias/edit.html", form=form, title="Editar Categoría")

        # Actualizar datos
        categoria.nombre = form.nombre.data.strip()
        categoria.descripcion = form.descripcion.data.strip() if form.descripcion.data else None
        categoria.estatus_visible = True  # si siempre debe estar activa al editar, o cambiar a form.estatus_visible.data
        db.session.commit()
        flash("Categoría actualizada correctamente", "success")
        return redirect(url_for("categorias_bp.index"))

    return render_template("produccion/categorias/edit.html", form=form, title="Editar Categoría")


# 🔹 DESACTIVAR / ACTIVAR CATEGORÍA
@categorias_bp.route("/delete/<uuid_categoria>", methods=["POST"])
def delete(uuid_categoria):
    categoria = Categoria.query.get_or_404(uuid_categoria)
    categoria.estatus_visible = not categoria.estatus_visible
    db.session.commit()

    estado = "activada" if categoria.estatus_visible else "desactivada"
    flash(f"Categoría {estado} correctamente", "success")
    return redirect(url_for("categorias_bp.index"))