from flask import render_template, redirect, url_for, flash, request
from flask_security import login_required, roles_accepted, current_user
from sqlalchemy.orm import joinedload
from decimal import Decimal, InvalidOperation

from . import pedidos_proveedor_bp
from .forms import PedidoProveedorForm
from app.utils.database_connection import db
from app.models.pedidos_proveedor import PedidoProveedorEncabezado, PedidoProveedorDetalle
from app.models.proveedores import Proveedor
from app.models.insumos import Insumo

@pedidos_proveedor_bp.route("/")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():
    busqueda = request.args.get("q")
    query = PedidoProveedorEncabezado.query.options(
        joinedload(PedidoProveedorEncabezado.proveedor),
        joinedload(PedidoProveedorEncabezado.usuario_solicita)
    )

    if busqueda:
        query = query.join(PedidoProveedorEncabezado.proveedor).filter(
            db.or_(
                PedidoProveedorEncabezado.folio_pedido.ilike(f"%{busqueda}%"),
                db.func.lower(Proveedor.razon_social).ilike(f"%{busqueda.lower()}%")
            )
        )

    pedidos = query.order_by(PedidoProveedorEncabezado.fecha_pedido.desc()).all()
    return render_template("produccion/pedidos_proveedor/index.html", pedidos=pedidos)

@pedidos_proveedor_bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def create():
    form = PedidoProveedorForm()
    proveedores = Proveedor.query.all()
    form.uuid_proveedor.choices = [(p.uuid_proveedor, f"{p.razon_social} - {p.rfc}") for p in proveedores]

    # Pre-llenado de proveedor si viene en la URL
    if request.method == "GET" and request.args.get('uuid_proveedor'):
        form.uuid_proveedor.data = request.args.get('uuid_proveedor')

    if request.method == "POST":
        try:
            insumos_ids = request.form.getlist("uuid_insumo[]")
            cantidades = request.form.getlist("cantidad[]")
            costos = request.form.getlist("costo[]")

            if not insumos_ids:
                flash("Agrega al menos un insumo al pedido.", "error")
                return redirect(url_for("pedidos_proveedor_bp.create"))

            # Validar folio unico
            if PedidoProveedorEncabezado.query.filter_by(folio_pedido=form.folio_pedido.data).first():
                flash("El folio de pedido ya existe.", "error")
                return redirect(url_for("pedidos_proveedor_bp.create"))

            nuevo_pedido = PedidoProveedorEncabezado(
                folio_pedido=form.folio_pedido.data,
                uuid_proveedor=form.uuid_proveedor.data,
                uuid_usuario_solicita=current_user.uuid_usuario,
                estatus=form.estatus.data or 'Pendiente'
            )
            db.session.add(nuevo_pedido)
            db.session.flush()
            
            proveedor_obj = Proveedor.query.get(form.uuid_proveedor.data)

            for i in range(len(insumos_ids)):
                if not insumos_ids[i]:
                    continue
                try:
                    cantidad = Decimal(cantidades[i])
                    costo = Decimal(costos[i])
                except (InvalidOperation, TypeError):
                    flash("Cantidad o costo estimado inválidos en insumos.", "error")
                    db.session.rollback()
                    return redirect(url_for("pedidos_proveedor_bp.create"))
                
                if cantidad <= 0 or costo <= 0:
                    flash("Las cantidades y los costos deben ser mayores a 0.", "error")
                    db.session.rollback()
                    return redirect(url_for("pedidos_proveedor_bp.create"))
                
                insumo = Insumo.query.get(insumos_ids[i])
                if not insumo:
                    flash("Insumo no encontrado.", "error")
                    db.session.rollback()
                    return redirect(url_for("pedidos_proveedor_bp.create"))

                # Validar que si es pieza, la cantidad sea entera
                if insumo.unidad_medida == 'PIEZA':
                    if cantidad % 1 != 0:
                        flash(f"El insumo '{insumo.nombre}' se compra por piezas. La cantidad debe ser un número entero.", "error")
                        db.session.rollback()
                        return redirect(url_for("pedidos_proveedor_bp.create"))

                

                detalle = PedidoProveedorDetalle(
                    uuid_pedido=nuevo_pedido.uuid_pedido,
                    uuid_insumo=insumos_ids[i],
                    cantidad_pedida=cantidad,
                    costo_unitario_estimado=costo
                )
                db.session.add(detalle)
            
            if nuevo_pedido.estatus == 'Aprobado':
                from app.models.compras import CompraEncabezado, CompraDetalle
                compra = CompraEncabezado(
                    folio_factura=nuevo_pedido.folio_pedido + "-COMPRA",
                    uuid_proveedor=nuevo_pedido.uuid_proveedor,
                    uuid_usuario_registro=current_user.uuid_usuario,
                    uuid_pedido=nuevo_pedido.uuid_pedido,
                    estatus='PENDIENTE'
                )
                db.session.add(compra)
                db.session.flush()
                for d in nuevo_pedido.detalles:
                    cd = CompraDetalle(
                        uuid_compra=compra.uuid_compra,
                        uuid_insumo=d.uuid_insumo,
                        cantidad_comprada=d.cantidad_pedida,
                        costo_unitario_compra=d.costo_unitario_estimado
                    )
                    db.session.add(cd)

            db.session.commit()
            flash("Pedido a proveedor registrado exitosamente.", "success")
            return redirect(url_for("pedidos_proveedor_bp.index"))
            
        except Exception as e:
            db.session.rollback()
            print("ERROR AL CREAR PEDIDO PROVEEDOR:", e)
            flash("Ocurrió un error al guardar el pedido a proveedor.", "error")
            return redirect(url_for("pedidos_proveedor_bp.create"))

    return render_template(
        "produccion/pedidos_proveedor/create.html",
        form=form,
        insumos=Insumo.query.all()
    )

@pedidos_proveedor_bp.route("/<uuid_pedido>")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def ver(uuid_pedido):
    pedido = PedidoProveedorEncabezado.query.options(
        joinedload(PedidoProveedorEncabezado.detalles)
        .joinedload(PedidoProveedorDetalle.insumo)
    ).get_or_404(uuid_pedido)
    
    total_estimado = Decimal(0)
    for d in pedido.detalles:
        sub = (d.cantidad_pedida or Decimal(0)) * (d.costo_unitario_estimado or Decimal(0))
        total_estimado += sub

    return render_template(
        "produccion/pedidos_proveedor/ver.html",
        pedido=pedido,
        total_estimado=total_estimado
    )

@pedidos_proveedor_bp.route("/aprobar/<uuid_pedido>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def aprobar(uuid_pedido):
    pedido = PedidoProveedorEncabezado.query.get_or_404(uuid_pedido)
    if pedido.estatus != 'Pendiente':
        flash('Solo se pueden aprobar pedidos pendientes.', 'error')
        return redirect(url_for('pedidos_proveedor_bp.ver', uuid_pedido=uuid_pedido))
    
    pedido.estatus = 'Aprobado'
    
    from app.models.compras import CompraEncabezado, CompraDetalle
    compra = CompraEncabezado(
        folio_factura=pedido.folio_pedido + "-COMPRA",
        uuid_proveedor=pedido.uuid_proveedor,
        uuid_usuario_registro=current_user.uuid_usuario,
        uuid_pedido=pedido.uuid_pedido,
        estatus='PENDIENTE'
    )
    db.session.add(compra)
    db.session.flush()
    for d in pedido.detalles:
        cd = CompraDetalle(
            uuid_compra=compra.uuid_compra,
            uuid_insumo=d.uuid_insumo,
            cantidad_comprada=d.cantidad_pedida,
            costo_unitario_compra=d.costo_unitario_estimado
        )
        db.session.add(cd)
    
    db.session.commit()
    flash('Pedido aprobado y Compra Pendiente generada automáticamente.', 'success')
    return redirect(url_for('pedidos_proveedor_bp.index'))

@pedidos_proveedor_bp.route("/rechazar/<uuid_pedido>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def rechazar(uuid_pedido):
    pedido = PedidoProveedorEncabezado.query.get_or_404(uuid_pedido)
    if pedido.estatus != 'Pendiente':
        flash('Solo se pueden rechazar pedidos pendientes.', 'error')
        return redirect(url_for('pedidos_proveedor_bp.ver', uuid_pedido=uuid_pedido))
    
    pedido.estatus = 'Cancelado'
    db.session.commit()
    flash('Pedido cancelado.', 'success')
    return redirect(url_for('pedidos_proveedor_bp.index'))

@pedidos_proveedor_bp.route("/completar/<uuid_pedido>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def completar(uuid_pedido):
    pedido = PedidoProveedorEncabezado.query.get_or_404(uuid_pedido)
    if pedido.estatus != 'Aprobado':
        flash('Solo se pueden completar pedidos aprobados.', 'error')
        return redirect(url_for('pedidos_proveedor_bp.ver', uuid_pedido=uuid_pedido))
    
    # Validar que no haya compras pendientes vinculadas
    compras_pendientes = [c for c in pedido.compras if c.estatus == 'PENDIENTE']
    if compras_pendientes:
        flash(f'No se puede completar el pedido porque tiene {len(compras_pendientes)} recepciones de mercancía (compras) pendientes.', 'error')
        return redirect(url_for('pedidos_proveedor_bp.ver', uuid_pedido=uuid_pedido))

    pedido.estatus = 'Completado'
    db.session.commit()
    flash('Pedido marcado como completado manualmente.', 'success')
    return redirect(url_for('pedidos_proveedor_bp.ver', uuid_pedido=uuid_pedido))
