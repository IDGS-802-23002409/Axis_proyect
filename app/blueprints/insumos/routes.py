from . import insumos_bp
from flask_security import login_required, roles_required, hash_password,roles_accepted
from app.models.insumos import Insumo
from .forms import InsumoForm
from app.utils.database_connection import db
from app.models.categorias import Categoria
from app.models.compras import CompraDetalle, CompraEncabezado
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import or_, func




# COSTO PROMEDIO
def calcular_costo_promedio(insumo_id, limite=5):
    ultimos_costos = (
        db.session.query(CompraDetalle.costo_unitario_compra)
        .join(CompraEncabezado, CompraDetalle.uuid_compra == CompraEncabezado.uuid_compra)
        .filter(
            CompraDetalle.uuid_insumo == insumo_id,
            CompraEncabezado.estatus == 'RECIBIDO'
        )
        .order_by(CompraEncabezado.fecha_compra.desc())
        .limit(limite)
        .all()
    )

    costos = [float(c[0]) for c in ultimos_costos if c[0] is not None]

    if not costos:
        return 0

    return sum(costos) / len(costos)


# INDEX

@insumos_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')  # cualquiera de los dos roles puede acceder
def index():
    busqueda = request.args.get("q")
    categoria = request.args.get("categoria")

    query = Insumo.query.filter(Insumo.estatus == 'ACTIVO')

    # categorías
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

    # filtro por categoría
    if categoria:
        query = query.join(Insumo.categoria).filter(
            Categoria.nombre == categoria
        )

    insumos = query.all()

    
    # COSTO PROMEDIO POR INSUMO
    
    for insumo in insumos:
        insumo.costo_promedio = calcular_costo_promedio(insumo.uuid_insumo)

  
    # COSTO PROMEDIO DE LOS INSUMOS ACUMULADO

    valorizado_total = sum(
        insumo.costo_promedio * float(insumo.stock_total_acumulado or 0)
        for insumo in insumos
    )

    return render_template(
        "produccion/insumos/index.html",
        insumos=insumos,
        categorias=categorias,
        valorizado_total=valorizado_total
    )

@insumos_bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def create():
    form = InsumoForm()

    categorias = Categoria.query.all()
    form.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
        (c.uuid_categoria, c.nombre) for c in categorias
    ]

    if form.validate_on_submit():
        categoria_uuid = form.uuid_categoria.data or None

        nombre = form.nombre.data.strip()
        sku = form.sku.data.strip() if form.sku.data else None
        unidad = form.unidad_medida.data


        # Nombre único
        if Insumo.query.filter_by(nombre=nombre).first():
            form.nombre.errors.append("Ya existe un insumo con ese nombre")
            flash("Error: el nombre ya existe", "error")
            return render_template("produccion/insumos/create.html", form=form)

        # SKU único
        if sku and Insumo.query.filter_by(sku=sku).first():
            form.sku.errors.append("Ya existe un insumo con ese SKU")
            flash("Error: el SKU ya existe", "error")
            return render_template("produccion/insumos/create.html", form=form)


        #  CASO PIEZA
        if unidad == "PIEZA":
            contenido_cantidad = 1
            contenido_unidad = "PIEZA"
            ancho = None

        #  CASO ROLLO
        elif unidad == "ROLLO":

            contenido_cantidad = form.contenido_cantidad.data
            ancho = form.ancho.data

            #  FORZAR UNIDAD CORRECTA
            contenido_unidad = "METRO"

            # VALIDAR CANTIDAD
            if contenido_cantidad is None or contenido_cantidad <= 0:
                form.contenido_cantidad.errors.append("Debe ser mayor a 0")
                flash("Error: la cantidad debe ser mayor a 0", "error")
                return render_template("produccion/insumos/create.html", form=form)

            # VALIDAR ANCHO
            if ancho is None or ancho <= 0:
                form.ancho.errors.append("El ancho es obligatorio para rollos")
                flash("Error: el ancho es obligatorio para rollos", "error")
                return render_template("produccion/insumos/create.html", form=form)

        else:
            flash("Unidad no válida", "error")
            return render_template("produccion/insumos/create.html", form=form)


        if unidad == "PIEZA" and contenido_unidad != "PIEZA":
            flash("Error: una pieza solo puede medirse en PIEZA", "error")
            return render_template("produccion/insumos/create.html", form=form)

        if unidad == "ROLLO" and contenido_unidad != "METRO":
            flash("Error: un rollo solo puede medirse en METRO", "error")
            return render_template("produccion/insumos/create.html", form=form)


        try:
            nuevo_insumo = Insumo(
                sku=sku,
                nombre=nombre,
                uuid_categoria=categoria_uuid,

                unidad_medida=unidad,
                contenido_cantidad=contenido_cantidad,
                contenido_unidad_medida=contenido_unidad,

                ancho=ancho,

                stock_total_acumulado=0,
                stock_minimo_alerta=form.stock_minimo_alerta.data or 0
            )

            db.session.add(nuevo_insumo)
            db.session.commit()

            flash("Insumo registrado correctamente", "success")

            if form.submit.data:
                return redirect(url_for('insumos_bp.index'))

            if form.submit_add.data:
                return redirect(url_for('insumos_bp.create'))

        except Exception as e:
            db.session.rollback()
            flash("Error al guardar el insumo", "error")
            print(e)

    return render_template("produccion/insumos/create.html", form=form)

#EDITAR

@insumos_bp.route("/edit/<string:uuid_insumo>", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def edit(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)
    form = InsumoForm(obj=insumo)

    categorias = Categoria.query.all()
    form.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
        (c.uuid_categoria, c.nombre) for c in categorias
    ]

    if form.validate_on_submit():

        categoria_uuid = form.uuid_categoria.data or None

        nombre = form.nombre.data.strip()
        sku = form.sku.data.strip() if form.sku.data else None
        unidad = form.unidad_medida.data

        # =========================
        # VALIDACIONES
        # =========================

        # Nombre único
        existe_nombre = Insumo.query.filter(
            Insumo.nombre == nombre,
            Insumo.uuid_insumo != uuid_insumo
        ).first()

        if existe_nombre:
            form.nombre.errors.append("Ya existe un insumo con ese nombre")
            flash("Error: el nombre ya existe", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # SKU único
        if sku:
            existe_sku = Insumo.query.filter(
                Insumo.sku == sku,
                Insumo.uuid_insumo != uuid_insumo
            ).first()

            if existe_sku:
                form.sku.errors.append("Ya existe un insumo con ese SKU")
                flash("Error: el SKU ya existe", "error")
                return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # =========================
        # CONFIGURACIÓN SEGÚN UNIDAD
        # =========================

        #  PIEZA
        if unidad == "PIEZA":
            contenido_cantidad = 1
            contenido_unidad = "PIEZA"
            ancho = None  #  limpiar ancho

        #  ROLLO
        elif unidad == "ROLLO":
            contenido_cantidad = form.contenido_cantidad.data
            ancho = form.ancho.data

            #  FORZAR
            contenido_unidad = "METRO"

            # VALIDAR CANTIDAD
            if contenido_cantidad is None or contenido_cantidad <= 0:
                form.contenido_cantidad.errors.append("Debe ser mayor a 0")
                flash("Error: la cantidad debe ser mayor a 0", "error")
                return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

            # VALIDAR ANCHO
            if ancho is None or ancho <= 0:
                form.ancho.errors.append("El ancho es obligatorio para rollos")
                flash("Error: el ancho es obligatorio", "error")
                return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        else:
            flash("Unidad no válida", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # =========================
        # VALIDACIÓN FINAL
        # =========================

        if unidad == "PIEZA" and contenido_unidad != "PIEZA":
            flash("Error: una pieza solo puede medirse en PIEZA", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        if unidad == "ROLLO" and contenido_unidad != "METRO":
            flash("Error: un rollo solo puede medirse en METRO", "error")
            return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

        # =========================
        # ACTUALIZACIÓN
        # =========================

        try:
            insumo.sku = sku
            insumo.nombre = nombre
            insumo.uuid_categoria = categoria_uuid

            insumo.unidad_medida = unidad
            insumo.contenido_cantidad = contenido_cantidad
            insumo.contenido_unidad_medida = contenido_unidad

            insumo.ancho = ancho  #  AQUÍ SE ACTUALIZA

            insumo.stock_minimo_alerta = form.stock_minimo_alerta.data or 0

            db.session.commit()

            flash("Insumo actualizado correctamente", "success")
            return redirect(url_for('insumos_bp.index'))

        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar el insumo", "error")
            print(e)

    else:
        if form.is_submitted():
            print("ERRORES:", form.errors)

    return render_template("produccion/insumos/edit.html", form=form, insumo=insumo)

#VER
@insumos_bp.route("/ver/<string:uuid_insumo>")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def view(uuid_insumo):
    insumo = Insumo.query.get_or_404(uuid_insumo)
    return render_template("produccion/insumos/ver.html", insumo=insumo)

#ELIMINACION LOGICA
@insumos_bp.route("/delete/<string:uuid_insumo>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
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

    flash("Insumo eliminado correctamente", "success")
    return redirect(url_for('insumos_bp.index'))

@insumos_bp.route("/restore/<string:uuid_insumo>", methods=["POST"])
@login_required
@roles_required('admin')
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
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def trash():
    insumos = Insumo.query.filter_by(estatus='INACTIVO').all()
    return render_template("produccion/insumos/trash.html", insumos=insumos)