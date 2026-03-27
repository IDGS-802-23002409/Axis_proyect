from . import insumos_bp
from app.models.insumos import Insumo
from .forms import InsumoForm
from app.utils.database_connection import db
from app.models.categorias import Categoria
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import or_, func

@insumos_bp.route("/")
def index():
    busqueda = request.args.get("q")
    categoria = request.args.get("categoria")

    query = Insumo.query.filter(Insumo.estatus == 'ACTIVO')

    # categorías (desde la tabla relacionada)
    categorias = db.session.query(Categoria.nombre).distinct().all()
    categorias = [c[0] for c in categorias]

    # búsqueda
    if busqueda:
        busqueda_like = f"%{busqueda.lower()}%"

        query = query.filter(
            or_(
                func.lower(Insumo.nombre).like(busqueda_like),
                func.lower(Insumo.sku).like(busqueda_like)
            )
        )

    # filtro por categoría (RELACIÓN)
    if categoria:
        query = query.join(Insumo.categoria).filter(
            Categoria.nombre == categoria
        )

    insumos = query.all()

    return render_template(
        "produccion/insumos/index.html",
        insumos=insumos,
        categorias=categorias
    )

#CREAR
@insumos_bp.route("/create", methods=["GET", "POST"])
def create():
    form = InsumoForm()

    categorias = Categoria.query.all()
    form.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
        (c.uuid_categoria, c.nombre) for c in categorias
    ]

    if form.validate_on_submit():

        categoria_uuid = form.uuid_categoria.data or None

        # VALIDACIONES
        if Insumo.query.filter_by(nombre=form.nombre.data).first():
            form.nombre.errors.append("Ya existe un insumo con ese nombre")
            flash("Error: el nombre ya existe", "error")
            return render_template("produccion/insumos/create.html", form=form)

        if form.sku.data and Insumo.query.filter_by(sku=form.sku.data).first():
            form.sku.errors.append("Ya existe un insumo con ese SKU")
            flash("Error: el SKU ya existe", "error")
            return render_template("produccion/insumos/create.html", form=form)
        if not form.unidad_medida.data:
            flash("Debe seleccionar una unidad de medida", "error")
            return render_template("produccion/insumos/create.html", form=form)

        nuevo_insumo = Insumo(
            sku=form.sku.data,
            nombre=form.nombre.data,
            uuid_categoria=categoria_uuid,
            unidad_medida=form.unidad_medida.data,  
            stock_total_acumulado=0,
            stock_minimo_alerta=form.stock_minimo_alerta.data
        )
        db.session.add(nuevo_insumo)
        db.session.commit()

        flash("Insumo registrado correctamente", "success")

        # BOTONES
        if form.submit.data:
            return redirect(url_for('insumos_bp.index'))

        elif form.submit_add.data:
            return redirect(url_for('insumos_bp.create'))

    return render_template("produccion/insumos/create.html", form=form)

#EDITAR
@insumos_bp.route("/edit/<string:uuid_insumo>", methods=["GET", "POST"])
def edit(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)
    form = InsumoForm(obj=insumo)

    # Cargar categorías
    categorias = Categoria.query.all()
    form.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
        (c.uuid_categoria, c.nombre) for c in categorias
    ]

    if form.validate_on_submit():

        categoria_uuid = form.uuid_categoria.data or None

        # VALIDAR NOMBRE (excepto el mismo registro)
        existe_nombre = Insumo.query.filter(
            Insumo.nombre == form.nombre.data,
            Insumo.uuid_insumo != uuid_insumo
        ).first()

        if existe_nombre:
            form.nombre.errors.append("Ya existe un insumo con ese nombre")
            flash("Error: el nombre ya existe", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # ACTUALIZAR CAMPOS PERMITIDOS
        insumo.nombre = form.nombre.data
        insumo.uuid_categoria = categoria_uuid
        insumo.unidad_medida = form.unidad_medida.data
        insumo.stock_minimo_alerta = form.stock_minimo_alerta.data

        db.session.commit()

        flash("Insumo actualizado correctamente", "success")
        return redirect(url_for('insumos_bp.index'))

    return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

#VER
@insumos_bp.route("/ver/<string:uuid_insumo>")
def view(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)
    return render_template("produccion/insumos/ver.html", insumo=insumo)

#ELIMINACION LOGICA
@insumos_bp.route("/delete/<string:uuid_insumo>", methods=["POST"])
def delete(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)

    # Evitar doble eliminación
    if insumo.estatus == 'INACTIVO':
        flash("El insumo ya está inactivo", "warning")
        return redirect(url_for('insumos_bp.index'))

    # Validaciones de negocio 
    if insumo.stock_total_acumulado > 0:
        flash("No puedes desactivar un insumo con stock disponible", "error")
        return redirect(url_for('insumos_bp.index'))

    #  AQUÍ NO SE BORRA, SOLO SE DESACTIVA
    insumo.estatus = 'INACTIVO'

    db.session.commit()

    flash("Insumo desactivado correctamente", "success")
    return redirect(url_for('insumos_bp.index'))

@insumos_bp.route("/restore/<string:uuid_insumo>", methods=["POST"])
def restore(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)

    if insumo.estatus == 'ACTIVO':
        flash("El insumo ya está activo", "warning")
        return redirect(url_for('insumos_bp.index'))

    insumo.estatus = 'ACTIVO'
    db.session.commit()

    flash("Insumo reactivado correctamente", "success")
    return redirect(url_for('insumos_bp.index'))

@insumos_bp.route("/trash")
def trash():
    insumos = Insumo.query.filter_by(estatus='INACTIVO').all()
    return render_template("produccion/insumos/trash.html", insumos=insumos)