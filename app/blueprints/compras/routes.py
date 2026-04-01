from . import compras_bp
from app.utils.database_connection import db
from app.models.compras import CompraEncabezado, CompraDetalle
from app.models.insumos import Insumo
from app.models.proveedores import Proveedor
from app.models.inventario import RolloInventario  # ajusta si cambia
from .forms import CompraEncabezadoForm
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import or_, func
from decimal import Decimal
from sqlalchemy.orm import joinedload



@compras_bp.route("/")
def index():
    busqueda = request.args.get("q")

    query = CompraEncabezado.query.options(
        joinedload(CompraEncabezado.proveedor),
        joinedload(CompraEncabezado.usuario_registro)
    )

    #  FILTRO
    if busqueda:
        query = query.join(CompraEncabezado.proveedor).filter(
            db.or_(
                CompraEncabezado.folio_factura.ilike(f"%{busqueda}%"),
                #  usa el campo correcto del proveedor
                # cambia 'nombre' por 'razon_social' si así se llama en tu modelo
                db.func.lower(CompraEncabezado.proveedor.has().property.mapper.class_.razon_social).ilike(f"%{busqueda.lower()}%")
            )
        )

    compras = query.order_by(CompraEncabezado.fecha_compra.desc()).all()

    return render_template("produccion/compras/index.html", compras=compras)

#CREATE
from decimal import Decimal, InvalidOperation


@compras_bp.route("/create", methods=["GET", "POST"])
def create():
    form = CompraEncabezadoForm()

    # PROVEEDORES
    proveedores = Proveedor.query.all()
    form.uuid_proveedor.choices = [
        (p.uuid_proveedor, f"{p.razon_social} - {p.rfc}") for p in proveedores
    ]

    # ESTATUS
    form.estatus.choices = [
        ("PENDIENTE", "Pendiente"),
        ("RECIBIDO", "Recibido")
    ]

    if request.method == "POST":
        try:
            insumos_ids = request.form.getlist("uuid_insumo[]")
            cantidades = request.form.getlist("cantidad[]")
            costos = request.form.getlist("costo[]")

            # =========================
            # VALIDACIÓN GENERAL
            # =========================
            if not insumos_ids:
                flash("Agrega al menos un insumo", "error")
                return redirect(url_for("compras_bp.create"))

            # =========================
            # CREAR ENCABEZADO
            # =========================
            nueva_compra = CompraEncabezado(
                folio_factura=form.folio_factura.data,
                uuid_proveedor=form.uuid_proveedor.data,
                uuid_usuario_registro="00000000-0000-0000-0000-000000000001",
                estatus=form.estatus.data or "PENDIENTE",
            )

            db.session.add(nueva_compra)
            db.session.flush()

            # IMPORTANTE: bandera clara
            es_recibido = nueva_compra.estatus == "RECIBIDO"

            # =========================
            # DETALLES
            # =========================
            for i in range(len(insumos_ids)):

                if not insumos_ids[i]:
                    continue

                # VALIDAR NUMÉRICOS
                try:
                    cantidad = Decimal(cantidades[i])
                    costo = Decimal(costos[i])
                except (InvalidOperation, TypeError):
                    flash("Cantidad o costo inválido", "error")
                    return redirect(url_for("compras_bp.create"))

                if cantidad <= 0:
                    flash("La cantidad debe ser mayor a 0", "error")
                    return redirect(url_for("compras_bp.create"))

                if costo < 0:
                    flash("El costo no puede ser negativo", "error")
                    return redirect(url_for("compras_bp.create"))

                # OBTENER INSUMO
                insumo = Insumo.query.get(insumos_ids[i])
                if not insumo:
                    flash("Insumo no encontrado", "error")
                    return redirect(url_for("compras_bp.create"))

                # CREAR DETALLE
                detalle = CompraDetalle(
                    uuid_compra=nueva_compra.uuid_compra,
                    uuid_insumo=insumo.uuid_insumo,
                    cantidad_comprada=cantidad,
                    costo_unitario_compra=costo,
                )
                db.session.add(detalle)
                db.session.flush()

                # =========================
                # SOLO SI ES RECIBIDO
                # =========================
                if es_recibido:

                    #  CALCULAR STOCK BASE
                    if insumo.unidad_medida == "PIEZA":
                        cantidad_base = cantidad

                    elif insumo.unidad_medida == "ROLLO":
                        cantidad_base = cantidad * Decimal(insumo.contenido_cantidad)

                    else:
                        cantidad_base = cantidad

                    #  ACTUALIZAR STOCK
                    insumo.stock_total_acumulado += cantidad_base

                    # =========================
                    # CREAR ROLLOS
                    # =========================
                    if insumo.unidad_medida == "ROLLO":

                        #  VALIDACIÓN REAL DEL ANCHO
                        if insumo.ancho is None:
                            flash(f"El insumo '{insumo.nombre}' no tiene ancho definido", "error")
                            return redirect(url_for("compras_bp.create"))

                        try:
                            ancho_real = Decimal(insumo.ancho)
                        except (InvalidOperation, TypeError):
                            flash(f"El ancho del insumo '{insumo.nombre}' es inválido", "error")
                            return redirect(url_for("compras_bp.create"))

                        if ancho_real <= 0:
                            flash(f"El ancho del insumo '{insumo.nombre}' debe ser mayor a 0", "error")
                            return redirect(url_for("compras_bp.create"))

                        #  CREACIÓN DE ROLLOS
                        for _ in range(int(cantidad)):

                            rollo = RolloInventario(
                                uuid_insumo=insumo.uuid_insumo,
                                uuid_detalle_compra=detalle.uuid_detalle_compra,
                                metraje_inicial=Decimal(insumo.contenido_cantidad),
                                metraje_continuo_actual=Decimal(insumo.contenido_cantidad),

                                #  AQUÍ SE MANDA CORRECTAMENTE
                                ancho_real_recibido=ancho_real
                            )

                            db.session.add(rollo)

            # =========================
            # COMMIT FINAL
            # =========================
            db.session.commit()

            flash("Compra creada correctamente", "success")
            return redirect(url_for("compras_bp.index"))

        except Exception as e:
            db.session.rollback()
            print("ERROR:", e)
            flash("Error al guardar la compra", "error")
            return redirect(url_for("compras_bp.create"))

    return render_template(
        "produccion/compras/create.html",
        form=form,
        insumos=Insumo.query.all()
    )


from decimal import Decimal
from sqlalchemy.orm import joinedload

@compras_bp.route("/<uuid_compra>")
def ver(uuid_compra):

    #aCargar TODO: encabezado → detalles → insumo
    compra = CompraEncabezado.query.options(
        joinedload(CompraEncabezado.detalles)
        .joinedload(CompraDetalle.insumo)
    ).get_or_404(uuid_compra)

    
    print("DETALLES:", len(compra.detalles))

    total_compra = Decimal(0)

    for d in compra.detalles:
        cantidad = d.cantidad_comprada or Decimal(0)
        costo = d.costo_unitario_compra or Decimal(0)

        print("Insumo:", d.insumo.nombre)
        print("Unidad:", d.insumo.unidad_medida)
        print("Cantidad:", cantidad)
        print("Costo:", costo)

        subtotal = cantidad * costo
        print("Subtotal:", subtotal)

        total_compra += subtotal

    print("TOTAL FINAL:", total_compra)

    return render_template(
        "produccion/compras/ver.html",
        compra=compra,
        total_compra=total_compra
    )
# =========================
# RECIBIR COMPRA
# =========================
@compras_bp.route("/recibir/<uuid_compra>", methods=["GET", "POST"])
def recibir(uuid_compra):
    compra = CompraEncabezado.query.get_or_404(uuid_compra)

    # SOLO PENDIENTE
    if compra.estatus != "PENDIENTE":
        flash("Solo se pueden recibir compras pendientes", "error")
        return redirect(url_for("compras_bp.index"))

    form = CompraEncabezadoForm(obj=compra)

    # PROVEEDORES
    proveedores = Proveedor.query.all()
    form.uuid_proveedor.choices = [
        (p.uuid_proveedor, f"{p.razon_social} - {p.rfc}") for p in proveedores
    ]

    if request.method == "POST":
        try:
            # TOMAR DETALLES EDITADOS
            insumos_ids = request.form.getlist("uuid_insumo[]")
            cantidades = request.form.getlist("cantidad[]")
            costos = request.form.getlist("costo[]")

            if not insumos_ids:
                flash("Agrega al menos un insumo", "error")
                return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

            # BORRAR DETALLES EXISTENTES (y ROLLOS)
            for detalle in compra.detalles:
                RolloInventario.query.filter_by(uuid_detalle_compra=detalle.uuid_detalle_compra).delete()
                db.session.delete(detalle)

            db.session.flush()

            # CREAR NUEVOS DETALLES
            for i in range(len(insumos_ids)):
                if not insumos_ids[i]:
                    continue

                try:
                    cantidad = Decimal(cantidades[i])
                    costo = Decimal(costos[i])
                except (InvalidOperation, TypeError):
                    flash("Cantidad o costo inválido", "error")
                    return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

                if cantidad <= 0 or costo < 0:
                    flash("Cantidad o costo inválido", "error")
                    return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

                insumo = Insumo.query.get(insumos_ids[i])
                if not insumo:
                    flash("Insumo no encontrado", "error")
                    return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

                detalle = CompraDetalle(
                    uuid_compra=compra.uuid_compra,
                    uuid_insumo=insumo.uuid_insumo,
                    cantidad_comprada=cantidad,
                    costo_unitario_compra=costo
                )
                db.session.add(detalle)
                db.session.flush()

                # =========================
                # ACTUALIZAR STOCK Y CREAR ROLLOS
                # =========================
                if insumo.unidad_medida == "PIEZA":
                    cantidad_base = cantidad
                elif insumo.unidad_medida == "ROLLO":
                    cantidad_base = cantidad * Decimal(insumo.contenido_cantidad)
                else:
                    cantidad_base = cantidad

                insumo.stock_total_acumulado += cantidad_base

                if insumo.unidad_medida == "ROLLO":
                    ancho_real = Decimal(insumo.ancho or 0)
                    for _ in range(int(cantidad)):
                        rollo = RolloInventario(
                            uuid_insumo=insumo.uuid_insumo,
                            uuid_detalle_compra=detalle.uuid_detalle_compra,
                            metraje_inicial=Decimal(insumo.contenido_cantidad),
                            metraje_continuo_actual=Decimal(insumo.contenido_cantidad),
                            ancho_real_recibido=ancho_real
                        )
                        db.session.add(rollo)

            # CAMBIAR ESTATUS
            compra.estatus = "RECIBIDO"
            db.session.commit()

            flash("Compra recibida correctamente y stock actualizado", "success")
            return redirect(url_for("compras_bp.index"))

        except Exception as e:
            db.session.rollback()
            print("ERROR:", e)
            flash("Error al recibir la compra", "error")
            return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

    return render_template(
        "produccion/compras/recibir.html",
        form=form,
        compra=compra,
        insumos=Insumo.query.all()
    )


# VER
@compras_bp.route("/ver/<string:uuid_compra>")
def view(uuid_compra):

    compra = CompraEncabezado.query.get_or_404(uuid_compra)

    return render_template("compras/ver.html", compra=compra)


# Cancelado
@compras_bp.route("/cancelar/<uuid_compra>", methods=["POST"])
def cancelar(uuid_compra):
    compra = CompraEncabezado.query.get_or_404(uuid_compra)

    # VALIDACIÓN IMPORTANTE
    if compra.estatus != "PENDIENTE":
        flash("Solo se pueden cancelar compras pendientes", "error")
        return redirect(url_for("compras_bp.index"))

    try:
        compra.estatus = "CANCELADO"

        db.session.commit()

        flash("Compra cancelada correctamente", "success")
        return redirect(url_for("compras_bp.index"))

    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        flash("Error al cancelar la compra", "error")
        return redirect(url_for("compras_bp.index"))


# compras canceladas
@compras_bp.route("/trash")
def trash():

    compras = (
        CompraEncabezado.query.filter_by(estatus="CANCELADO")
        .order_by(CompraEncabezado.fecha_compra.desc())
        .all()
    )

    return render_template("compras/trash.html", compras=compras)
