from . import compras_bp
from flask_security import login_required, roles_required, hash_password,roles_accepted
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
@login_required
@roles_accepted('admin', 'produccion')
def index():
    busqueda = request.args.get("q")

    query = CompraEncabezado.query.options(
        joinedload(CompraEncabezado.proveedor),
        joinedload(CompraEncabezado.usuario_registro)
    )

    if busqueda:
        query = query.join(CompraEncabezado.proveedor).filter(
            db.or_(
                CompraEncabezado.folio_factura.ilike(f"%{busqueda}%"),
                db.func.lower(Proveedor.razon_social).ilike(f"%{busqueda.lower()}%")
            )
        )

    compras = query.order_by(CompraEncabezado.fecha_compra.desc()).all()

    return render_template("produccion/compras/index.html", compras=compras)

#CREATE
from decimal import Decimal, InvalidOperation


from flask_security import current_user
from decimal import Decimal, InvalidOperation

@compras_bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'produccion')
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

            if not insumos_ids:
                flash("Agrega al menos un insumo", "error")
                return redirect(url_for("compras_bp.create"))

            # CREAR ENCABEZADO
            nueva_compra = CompraEncabezado(
                folio_factura=form.folio_factura.data,
                uuid_proveedor=form.uuid_proveedor.data,
                uuid_usuario_registro=current_user.uuid_usuario,  # ahora toma el usuario logueado
                estatus=form.estatus.data or "PENDIENTE",
            )

            db.session.add(nueva_compra)
            db.session.flush()

            es_recibido = nueva_compra.estatus == "RECIBIDO"

            # CREAR DETALLES
            for i in range(len(insumos_ids)):
                if not insumos_ids[i]:
                    continue

                try:
                    cantidad = Decimal(cantidades[i])
                    costo = Decimal(costos[i])
                except (InvalidOperation, TypeError):
                    flash("Cantidad o costo inválido", "error")
                    return redirect(url_for("compras_bp.create"))

                if cantidad <= 0 or costo < 0:
                    flash("Cantidad o costo inválido", "error")
                    return redirect(url_for("compras_bp.create"))

                insumo = Insumo.query.get(insumos_ids[i])
                if not insumo:
                    flash("Insumo no encontrado", "error")
                    return redirect(url_for("compras_bp.create"))

                detalle = CompraDetalle(
                    uuid_compra=nueva_compra.uuid_compra,
                    uuid_insumo=insumo.uuid_insumo,
                    cantidad_comprada=cantidad,
                    costo_unitario_compra=costo
                )
                db.session.add(detalle)
                db.session.flush()

                if es_recibido:
                    # CALCULAR STOCK
                    if insumo.unidad_medida == "PIEZA":
                        cantidad_base = cantidad
                    elif insumo.unidad_medida == "ROLLO":
                        cantidad_base = cantidad * Decimal(insumo.contenido_cantidad)
                    else:
                        cantidad_base = cantidad

                    insumo.stock_total_acumulado += cantidad_base

                    # CREAR ROLLOS (sin ancho)
                    if insumo.unidad_medida == "ROLLO":
                        for _ in range(int(cantidad)):
                            rollo = RolloInventario(
                                uuid_insumo=insumo.uuid_insumo,
                                uuid_detalle_compra=detalle.uuid_detalle_compra,
                                metraje_inicial=Decimal(insumo.contenido_cantidad),
                                metraje_continuo_actual=Decimal(insumo.contenido_cantidad)
                            )
                            db.session.add(rollo)

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
@login_required
@roles_accepted('admin', 'produccion')
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
@login_required
@roles_accepted('admin', 'produccion')
def recibir(uuid_compra):
    from app.models.pedidos_proveedor import PedidoProveedorEncabezado, PedidoProveedorDetalle

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
            # ── REGLA: Validación contra pedido formal ──────────────────
            # No se acepta material que no coincida exactamente con lo solicitado.
            if compra.uuid_pedido:
                pedido = PedidoProveedorEncabezado.query.get(compra.uuid_pedido)
                if pedido:
                    # Construir mapa {uuid_insumo: cantidad_pedida} del pedido
                    pedido_map = {
                        d.uuid_insumo: float(d.cantidad_pedida)
                        for d in pedido.detalles
                    }
                    # Verificar cada detalle de la compra contra el pedido
                    for detalle in compra.detalles:
                        if detalle.uuid_insumo not in pedido_map:
                            flash(
                                f"Rechazado: El insumo '{detalle.insumo.nombre}' no está en el pedido original. "
                                f"No se aceptan productos extra.",
                                "error"
                            )
                            return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))
                        
                        cantidad_comprada = float(detalle.cantidad_comprada)
                        cantidad_pedida = pedido_map[detalle.uuid_insumo]
                        if cantidad_comprada != cantidad_pedida:
                            flash(
                                f"Rechazado: La cantidad de '{detalle.insumo.nombre}' no coincide con el pedido. "
                                f"Pedido: {cantidad_pedida}, Compra: {cantidad_comprada}.",
                                "error"
                            )
                            return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

            # En la recepción no se pueden modificar insumos, cantidades ni costos.
            # Solo se verifica y se ingresa el metraje_real para rollos.
            metrajes_reales = request.form.getlist("metraje_real[]")

            # Validar tolerancia para rollos
            for i, detalle in enumerate(compra.detalles):
                insumo = detalle.insumo
                cantidad = detalle.cantidad_comprada

                if insumo.unidad_medida == "ROLLO":
                    try:
                        metraje_real = Decimal(metrajes_reales[i])
                    except (InvalidOperation, TypeError, IndexError):
                        flash("Metraje real inválido.", "error")
                        return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

                    metraje_esperado = cantidad * Decimal(insumo.contenido_cantidad)
                    tolerancia = cantidad * Decimal('0.05')

                    if abs(metraje_real - metraje_esperado) > tolerancia:
                        flash(f"Rechazado: {insumo.nombre} no cumple la tolerancia exacta (±5cm por rollo). Esperado: {metraje_esperado}m, Recibido: {metraje_real}m.", "error")
                        return redirect(url_for("compras_bp.recibir", uuid_compra=uuid_compra))

                    # Si es aceptado, actualizamos stock y creamos rollos
                    metraje_por_rollo = metraje_real / cantidad
                    insumo.stock_total_acumulado += metraje_real
                    
                    for _ in range(int(cantidad)):
                        rollo = RolloInventario(
                            uuid_insumo=insumo.uuid_insumo,
                            uuid_detalle_compra=detalle.uuid_detalle_compra,
                            metraje_inicial=metraje_por_rollo,
                            metraje_continuo_actual=metraje_por_rollo,
                        )
                        db.session.add(rollo)
                else:
                    # Insumos por pieza
                    insumo.stock_total_acumulado += cantidad

            # CAMBIAR ESTATUS
            compra.estatus = "RECIBIDO"
            db.session.commit()

            flash("Compra validada y recibida correctamente. Inventario actualizado.", "success")
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
@login_required
@roles_accepted('admin', 'produccion')
def view(uuid_compra):

    compra = CompraEncabezado.query.get_or_404(uuid_compra)

    return render_template("compras/ver.html", compra=compra)


# Cancelado
@compras_bp.route("/cancelar/<uuid_compra>", methods=["POST"])
@login_required
@roles_accepted('admin', 'produccion')
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
@login_required
@roles_accepted('admin', 'produccion')
def trash():

    compras = (
        CompraEncabezado.query.filter_by(estatus="CANCELADO")
        .order_by(CompraEncabezado.fecha_compra.desc())
        .all()
    )

    return render_template("compras/trash.html", compras=compras)
