from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_security import login_required, current_user
from app.utils.database_connection import db
from app.models.clientes import Cliente
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.ventas import VentaEncabezado, VentaDetalle
from datetime import datetime
import uuid
from decimal import Decimal

checkout_bp = Blueprint('checkout', __name__, template_folder='../../templates/client')

CART_SESSION_KEY = 'axis_cart'


def load_cart():
    """Carga el carrito desde la sesión Flask (por usuario/navegador)."""
    return session.get(CART_SESSION_KEY, [])


def save_cart(cart):
    """Guarda el carrito en la sesión Flask y marca la sesión como modificada."""
    session[CART_SESSION_KEY] = cart
    session.modified = True


def calculate_cart_totals(cart):
    subtotal = 0.0
    for item in cart:
        # Aseguramos que el precio sea numérico (limpiamos por si viene algo raro)
        try:
            p_val = item.get('price', 0.0)
            if p_val is None: p_val = 0.0
            price = float(p_val)
        except (ValueError, TypeError):
            price = 0.0
            
        try:
            q_val = item.get('quantity', 1)
            if q_val is None: q_val = 1
            quantity = int(q_val)
        except (ValueError, TypeError):
            quantity = 1
            
        subtotal += price * quantity
        
    shipping = 9.99 if (0 < subtotal < 100) else 0.0
    total = subtotal + shipping
    return {'subtotal': subtotal, 'shipping': shipping, 'total': total}


@checkout_bp.route('/carrito/agregar', methods=['POST'])
def agregar_carrito():
    uuid_explosion = request.form.get('uuid_producto')  # Del catálogo viene el ID de la receta/explosión
    try:
        cantidad = int(request.form.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 1

    if not uuid_explosion:
        flash('Producto no especificado', 'error')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    # Obtener la explosión para validar que existe
    explosion = ExplosionMaterialesCabecera.query.get(uuid_explosion)
    if not explosion or explosion.estatus != 'ACTIVO':
        flash('Lo sentimos, este producto no está disponible en este momento.', 'error')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    # Buscar un ProductoTerminado asociado a esta explosión que esté activo
    producto = ProductoTerminado.query.filter_by(uuid_explosion=uuid_explosion, active=True).first()
    
    if not producto:
        flash('Lo sentimos, este producto no está disponible en este momento.', 'error')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    stock_disponible = producto.stock_fisico_actual or 0
    # Eliminamos la restricción de stock aquí, ya que la regla permite comprar sin stock
    # con 5 días extra de entrega.

    cart = load_cart()
    total_quantity = sum(item.get('quantity', 0) for item in cart)
    
    if total_quantity + cantidad > 100:
        flash(f'No se pueden añadir {cantidad} unidades. El carrito tiene un límite máximo de 100 productos totales.', 'warning')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    if producto.precio_venta <= 0:
        flash('Este producto no tiene un precio configurado y no puede venderse.', 'error')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    # Buscar si ya existe este producto específico (por su uuid_producto real)
    existing_idx = None
    for idx, item in enumerate(cart):
        if item.get('uuid_producto') == producto.uuid_producto:
            existing_idx = idx
            break

    if existing_idx is not None:
        nueva_cantidad = cart[existing_idx]['quantity'] + cantidad
        if total_quantity + cantidad > 100: # Re-verificar por si acaso
             flash('El carrito no puede tener más de 100 productos en total.', 'error')
             return redirect(request.referrer or url_for('catalog.catalog_view'))
        cart[existing_idx]['quantity'] = nueva_cantidad
    else:
        cart.append({
            'uuid_producto': producto.uuid_producto,
            'uuid_explosion': producto.uuid_explosion,
            'nombre': explosion.nombre_receta if explosion else 'Producto',
            'talla': explosion.talla if explosion else 'Única',
            'price': float(producto.precio_venta),
            'image': producto.imagen_url if producto.imagen_url else '/static/images/default/default-image.png',
            'quantity': cantidad,
            'stock': stock_disponible
        })

    save_cart(cart)
    session['open_cart'] = True  # Flag para abrir el carrito en el frontend
    flash(f'¡{explosion.nombre_receta if explosion else "Producto"} añadido al carrito! ✓', 'success')
    return redirect(request.referrer or url_for('catalog.catalog_view'))


@checkout_bp.route('/carrito/actualizar', methods=['POST'])
def actualizar_carrito():
    uuid_producto = request.form.get('uuid_producto')
    try:
        cantidad = int(request.form.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 1
    talla = request.form.get('talla', 'M')

    if not uuid_producto:
        flash('Producto no especificado', 'error')
        return redirect(url_for('checkout.checkout_view'))

    producto = ProductoTerminado.query.get(uuid_producto)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('checkout.checkout_view'))

    cart = load_cart()
    total_quantity = sum(item.get('quantity', 0) for item in cart if item.get('uuid_producto') != uuid_producto)
    if total_quantity + cantidad > 100:
        flash('El carrito no puede tener más de 100 productos en total.', 'error')
        return redirect(url_for('checkout.checkout_view'))

    if cantidad <= 0:
        # Si cantidad es 0 o negativa, eliminar el item
        cart = [i for i in cart if not (i.get('uuid_producto') == uuid_producto)]
    else:
        for idx, item in enumerate(cart):
            if item.get('uuid_producto') == uuid_producto:
                cart[idx]['quantity'] = cantidad
                break

    save_cart(cart)
    return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/carrito/eliminar', methods=['POST'])
def eliminar_carrito():
    uuid_producto = request.form.get('uuid_producto')
    talla = request.form.get('talla', 'M')

    cart = load_cart()
    cart = [item for item in cart if not (item.get('uuid_producto') == uuid_producto and item.get('talla') == talla)]

    save_cart(cart)
    flash('Producto eliminado del carrito', 'success')
    return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/carrito/vaciar', methods=['POST'])
def vaciar_carrito():
    save_cart([])
    flash('Carrito vaciado', 'success')
    return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/checkout')
def checkout_view():
    cart = load_cart()
    totals = calculate_cart_totals(cart)

    # Si el usuario está autenticado pero no tiene perfil de cliente
    if current_user.is_authenticated and not current_user.cliente:
        flash('Por favor completa tu perfil para continuar', 'info')
        return redirect(url_for('checkout.completar_perfil'))

    return render_template('carrito.html', cart=cart, totals=totals)


@checkout_bp.route('/checkout/procesar', methods=['POST'])
@login_required
def procesar_checkout():
    import logging
    logger = logging.getLogger(__name__)
    
    logger.warning(f">>> [CHECKOUT] email={current_user.email}")
    logger.warning(f">>> [CHECKOUT] cliente={current_user.cliente}")
    logger.warning(f">>> [CHECKOUT] roles={[r.name for r in current_user.roles]}")
    
    if not current_user.cliente:
        logger.warning(">>> [CHECKOUT] REDIRIGE: sin cliente")
        flash('Por favor completa tu perfil primero', 'error')
        return redirect(url_for('checkout.completar_perfil'))
    logger.warning(f">>> [CHECKOUT] telefono={current_user.cliente.telefono}")
    logger.warning(f">>> [CHECKOUT] direccion={current_user.cliente.direccion_completa}")

    # REGLA: Datos obligatorios (Teléfono y Dirección)
    if not current_user.cliente.telefono or not current_user.cliente.direccion_completa:
        logger.warning(">>> [CHECKOUT] REDIRIGE: sin telefono/direccion")
        flash('Por favor actualiza tu teléfono y dirección en tu perfil antes de comprar.', 'warning')
        return redirect(url_for('checkout.mi_cuenta'))

    cart = load_cart()
    logger.warning(f">>> [CHECKOUT] cart={cart}")
    if not cart:
        logger.warning(">>> [CHECKOUT] REDIRIGE: carrito vacío")
        flash('El carrito está vacío', 'error')
        return redirect(url_for('checkout.checkout_view'))

    try:
        from app.models.produccion import OrdenProduccion
        from app.models.explosion_materiales import ExplosionMaterialesCabecera
        
        # Generar folio seguro (máx 25 caracteres según el modelo)
        # AXIS (4) + DATE (8) + - (1) + UUID[:6] (6) = 19 caracteres
        numero_pedido = f"AXIS-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
        
        # Determinar si el pedido completo será Pendiente o Completado
        # Regla: Si hay stock insuficiente en AL MENOS UN producto, el pedido queda Pendiente.
        estatus_global = 'Completado'
        mensajes_extra = []
        
        venta = VentaEncabezado(
            uuid_venta=str(uuid.uuid4()),
            numero_pedido=numero_pedido,
            uuid_cliente=current_user.cliente.uuid_cliente,
            metodo_pago=request.form.get('metodo_pago', 'Transferencia'),
            estatus_envio='Procesando' # Temporal
        )
        db.session.add(venta)
        db.session.flush()

        for item in cart:
            producto = ProductoTerminado.query.get(item['uuid_producto'])
            if not producto or not producto.active:
                flash(f'El producto {item["nombre"]} ya no está disponible', 'error')
                db.session.rollback()
                return redirect(url_for('checkout.checkout_view'))

            cantidad_pedida = int(item['quantity'])
            stock_actual = int(producto.stock_fisico_actual or 0)
            
            detalle = VentaDetalle(
                uuid_detalle=str(uuid.uuid4()),
                uuid_venta=venta.uuid_venta,
                uuid_producto=item['uuid_producto'],
                cantidad=cantidad_pedida,
                precio_unitario_historico=Decimal(str(item['price']))
            )
            db.session.add(detalle)
            db.session.flush()

            # REGLA: Política de Inventario "Express"
            # Pedidos pequeños (< 10): toman del stock disponible y crean OP por el faltante.
            # Pedidos grandes (>= 10) que superan stock: NO toman stock, crean OP completa
            #   para preservar inventario para ventas pequeñas.
            if cantidad_pedida > stock_actual:
                estatus_global = 'Pendiente'

                # Validar que tenga receta antes de crear OP
                receta = ExplosionMaterialesCabecera.query.filter_by(uuid_explosion=producto.uuid_explosion).first()
                if not receta:
                     flash(f"Error: El producto {producto.sku_especifico} no tiene una receta asignada. Contacte a soporte.", "error")
                     db.session.rollback()
                     return redirect(url_for('checkout.checkout_view'))

                if cantidad_pedida < 10 and stock_actual > 0:
                    faltante = cantidad_pedida - stock_actual
                    producto.stock_fisico_actual = 0
                    mensajes_extra.append(
                        f"{receta.nombre_receta}: {stock_actual} uds. del stock + "
                        f"{faltante} uds. entrarán a producción (+5 días entrega)."
                    )
                    cantidad_op_base = faltante
                else:
                    mensajes_extra.append(
                        f"{receta.nombre_receta} entrará a producción completa (+5 días entrega)."
                    )
                    cantidad_op_base = cantidad_pedida

                nueva_op = OrdenProduccion(
                    uuid_op=str(uuid.uuid4()),
                    uuid_producto=producto.uuid_producto,
                    uuid_venta_detalle=detalle.uuid_detalle,
                    cantidad_a_producir=cantidad_op_base,
                    estado='Pendiente'
                )
                db.session.add(nueva_op)
                db.session.flush()

                # Reserva de Materiales para la OP automática
                from app.models.insumos import Insumo
                from app.models.inventario import RolloInventario
                from app.models.produccion import EjecucionCorte
                
                for det_receta in receta.detalles:
                    consumo_unitario = Decimal(det_receta.consumo_teorico_unitario)
                    cantidad_total_necesaria = consumo_unitario * Decimal(cantidad_op_final)
                    insumo = Insumo.query.get(det_receta.uuid_insumo)
                    
                    if insumo.stock_total_acumulado < cantidad_total_necesaria:
                        mensajes_extra.append(f"Nota de producción: Pendiente de abastecimiento de {insumo.nombre}.")
                        continue # Saltamos la reserva automática, el admin la hará después
                    
                    insumo.stock_total_acumulado -= cantidad_total_necesaria

                    if insumo.unidad_medida == "ROLLO":
                        prendas_restantes = cantidad_op_final
                        rollos = RolloInventario.query.filter(
                            RolloInventario.uuid_insumo == det_receta.uuid_insumo,
                            RolloInventario.metraje_continuo_actual > 0
                        ).order_by(RolloInventario.fecha_creacion.asc()).all()

                        for rollo in rollos:
                            metraje_disponible = Decimal(rollo.metraje_continuo_actual)
                            prendas_de_este_rollo = int(metraje_disponible // consumo_unitario)

                            if prendas_de_este_rollo <= 0:
                                continue

                            prendas_a_usar = min(prendas_restantes, prendas_de_este_rollo)
                            metros_a_descontar = Decimal(prendas_a_usar) * consumo_unitario

                            rollo.metraje_continuo_actual -= metros_a_descontar

                            if rollo.metraje_continuo_actual <= Decimal('0.0001'):
                                rollo.metraje_continuo_actual = Decimal('0.0000')

                            corte = EjecucionCorte(
                                uuid_op=nueva_op.uuid_op,
                                uuid_rollo_used=rollo.uuid_rollo,
                                metros_teoricos_requeridos=metros_a_descontar,
                                metros_sacados_bodega=metros_a_descontar,
                                prendas_reales_logradas=prendas_a_usar
                            )
                            db.session.add(corte)

                            prendas_restantes -= prendas_a_usar
                            if prendas_restantes == 0:
                                break

                        if prendas_restantes > 0:
                            mensajes_extra.append(f"Nota para taller: Asegurar trazabilidad de rollo para {insumo.nombre}.")
                            # Se han descontado los cortes posibles, el resto quedará pendiente de asignar

            else:
                # Si hay stock suficiente: Se descuenta y queda como completado (si no hay otros pendientes)
                producto.stock_fisico_actual -= cantidad_pedida

        venta.estatus_envio = estatus_global
        db.session.commit()

        # Limpiar carrito
        save_cart([])

        for msg in mensajes_extra:
            flash(msg, 'info')
            
        flash(f'¡Pedido realizado! Número: {numero_pedido}', 'success')
        return redirect(url_for('checkout.pedido_exito', numero_pedido=numero_pedido))

    except Exception as e:
        db.session.rollback()
        import traceback
        logger.error(f">>> [CHECKOUT] ERROR COMPLETO:\n{traceback.format_exc()}")
        print(traceback.format_exc()) # Log para consola
        flash(f'Error al procesar el pedido (DB): {str(e)}', 'error')
        return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/checkout/exito/<numero_pedido>')
@login_required
def pedido_exito(numero_pedido):
    return render_template('pedido_exito.html', numero_pedido=numero_pedido)


@checkout_bp.route('/mi-cuenta', methods=['GET', 'POST'])
@login_required
def mi_cuenta():
    # Solo para clientes
    if not current_user.has_role('cliente'):
        return redirect(url_for('checkout.perfil'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion_completa')

        if not nombre or not email:
            flash('Nombre y Email son obligatorios', 'error')
            return redirect(url_for('checkout.mi_cuenta'))

        current_user.nombre_completo = nombre
        current_user.email = email
        
        cliente = current_user.cliente
        if not cliente:
            cliente = Cliente(uuid_usuario=current_user.uuid_usuario)
            db.session.add(cliente)
        
        cliente.telefono = telefono
        cliente.direccion_completa = direccion
        
        try:
            db.session.commit()
            flash('Información de cuenta actualizada ✓', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}', 'error')
            
        return redirect(url_for('checkout.mi_cuenta'))

    return render_template('cuenta.html')


@checkout_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    # Perfil simplificado para Admins en el panel de producción
    if not current_user.has_role('admin'):
        return redirect(url_for('checkout.mi_cuenta'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')

        current_user.nombre_completo = nombre
        current_user.email = email
        
        try:
            db.session.commit()
            flash('Perfil de administrador actualizado', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            
        return redirect(url_for('checkout.perfil'))

    return render_template('perfil.html')


@checkout_bp.route('/checkout/completar_perfil', methods=['GET', 'POST'])
@login_required
def completar_perfil():
    if current_user.cliente:
        return redirect(url_for('checkout.checkout_view'))

    if request.method == 'POST':
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion_completa')

        if not telefono or len(direccion or '') < 5:
            flash("Por favor proporcione un teléfono y una dirección válida.", "error")
            return render_template('completar_perfil.html')

        nuevo_cliente = Cliente(
            uuid_usuario=current_user.uuid_usuario,
            telefono=telefono,
            direccion_completa=direccion
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash("Perfil guardado. Continuemos con tu compra.", "success")
        return redirect(url_for('checkout.checkout_view'))

    return render_template('completar_perfil.html')