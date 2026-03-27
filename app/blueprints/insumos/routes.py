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

# CREAR
@insumos_bp.route("/create", methods=["GET", "POST"])
def create():
    form = InsumoForm()

    # 🔹 Cargar categorías
    categorias = Categoria.query.all()
    form.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
        (c.uuid_categoria, c.nombre) for c in categorias
    ]

    if form.validate_on_submit():

        categoria_uuid = form.uuid_categoria.data or None

        # 🔹 NORMALIZAR DATOS (clave para evitar duplicados raros)
        nombre = form.nombre.data.strip()
        sku = form.sku.data.strip() if form.sku.data else None

        # 🔹 VALIDACIONES
        if Insumo.query.filter_by(nombre=nombre).first():
            form.nombre.errors.append("Ya existe un insumo con ese nombre")
            flash("Error: el nombre ya existe", "error")
            return render_template("produccion/insumos/create.html", form=form)

        if sku and Insumo.query.filter_by(sku=sku).first():
            form.sku.errors.append("Ya existe un insumo con ese SKU")
            flash("Error: el SKU ya existe", "error")
            return render_template("produccion/insumos/create.html", form=form)

        # 🔹 VALIDACIÓN NUMÉRICA
        if form.contenido_cantidad.data is None or form.contenido_cantidad.data <= 0:
            form.contenido_cantidad.errors.append("Debe ser mayor a 0")
            flash("Error en cantidad por unidad", "error")
            return render_template("produccion/insumos/create.html", form=form)

        # 🔹 VALIDACIÓN LÓGICA (nivel pro 👇)
        if form.unidad_medida.data == "ROLLO" and form.contenido_unidad_medida.data != "METRO":
            flash("Un rollo normalmente se mide en metros", "warning")

        if form.unidad_medida.data == "CAJA" and form.contenido_unidad_medida.data != "PIEZA":
            flash("Una caja normalmente contiene piezas", "warning")

        try:
            # 🔹 CREACIÓN DEL INSUMO
            nuevo_insumo = Insumo(
                sku=sku,
                nombre=nombre,
                uuid_categoria=categoria_uuid,

                # CONFIGURACIÓN
                unidad_medida=form.unidad_medida.data,
                contenido_cantidad=form.contenido_cantidad.data,
                contenido_unidad_medida=form.contenido_unidad_medida.data,

                # INVENTARIO
                stock_total_acumulado=0,
                stock_minimo_alerta=form.stock_minimo_alerta.data or 0
            )

            db.session.add(nuevo_insumo)
            db.session.commit()

            flash("Insumo registrado correctamente", "success")

            # 🔹 BOTONES
            if form.submit.data:
                return redirect(url_for('insumos_bp.index'))

            elif form.submit_add.data:
                return redirect(url_for('insumos_bp.create'))

        except Exception as e:
            db.session.rollback()
            flash("Error al guardar el insumo", "error")
            print(e)  # útil para debug

    return render_template("produccion/insumos/create.html", form=form)

#EDITAR
@insumos_bp.route("/edit/<string:uuid_insumo>", methods=["GET", "POST"])
def edit(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)
    form = InsumoForm(obj=insumo)

    # 🔹 Cargar categorías
    categorias = Categoria.query.all()
    form.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
        (c.uuid_categoria, c.nombre) for c in categorias
    ]

    if form.validate_on_submit():

        categoria_uuid = form.uuid_categoria.data or None

        # 🔹 NORMALIZAR (igual que create)
        nombre = form.nombre.data.strip()
        sku = form.sku.data.strip() if form.sku.data else None

        # 🔹 VALIDAR NOMBRE (excluyendo el actual)
        existe_nombre = Insumo.query.filter(
            Insumo.nombre == nombre,
            Insumo.uuid_insumo != uuid_insumo
        ).first()

        if existe_nombre:
            form.nombre.errors.append("Ya existe un insumo con ese nombre")
            flash("Error: el nombre ya existe", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # 🔹 VALIDAR SKU (excluyendo el actual)
        if sku:
            existe_sku = Insumo.query.filter(
                Insumo.sku == sku,
                Insumo.uuid_insumo != uuid_insumo
            ).first()

            if existe_sku:
                form.sku.errors.append("Ya existe un insumo con ese SKU")
                flash("Error: el SKU ya existe", "error")
                return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # 🔹 VALIDACIÓN NUMÉRICA
        if form.contenido_cantidad.data is None or form.contenido_cantidad.data <= 0:
            form.contenido_cantidad.errors.append("Debe ser mayor a 0")
            flash("Error en cantidad por unidad", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # 🔹 VALIDACIÓN LÓGICA
        if form.unidad_medida.data == "ROLLO" and form.contenido_unidad_medida.data != "METRO":
            flash("Un rollo normalmente se mide en metros", "warning")

        if form.unidad_medida.data == "CAJA" and form.contenido_unidad_medida.data != "PIEZA":
            flash("Una caja normalmente contiene piezas", "warning")

        try:
            # 🔹 ACTUALIZAR TODO (aquí estaba tu error principal 👇)
            insumo.sku = sku
            insumo.nombre = nombre
            insumo.uuid_categoria = categoria_uuid

            insumo.unidad_medida = form.unidad_medida.data
            insumo.contenido_cantidad = form.contenido_cantidad.data
            insumo.contenido_unidad_medida = form.contenido_unidad_medida.data

            insumo.stock_minimo_alerta = form.stock_minimo_alerta.data or 0

            db.session.commit()

            flash("Insumo actualizado correctamente", "success")
            return redirect(url_for('insumos_bp.index'))

        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar el insumo", "error")
            print(e)

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