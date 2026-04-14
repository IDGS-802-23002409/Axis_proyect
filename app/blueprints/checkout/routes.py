from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_security import login_required, current_user
from app.utils.database_connection import db
from app.models.clientes import Cliente
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.ventas import VentaEncabezado, VentaDetalle
from app.models.pedidos_cliente import PedidoClienteEncabezado
from datetime import datetime
import uuid
from decimal import Decimal
import re

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
    session.pop('axis_discount', None)
    session.pop('discount_code', None)
    flash('Carrito vaciado', 'success')
    return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/carrito/descuento', methods=['POST'])
def aplicar_descuento():
    codigo = request.form.get('codigo', '').strip().upper()
    if codigo == 'AXIS10':
        session['axis_discount'] = 0.10
        session['discount_code'] = codigo
        flash('¡Cupón AXIS10 aplicado correctamente! 10% de descuento.', 'success')
    else:
        flash('Código de descuento inválido.', 'error')
    
    return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/carrito/quitar-descuento', methods=['POST'])
def quitar_descuento():
    session.pop('axis_discount', None)
    session.pop('discount_code', None)
    flash('Cupón eliminado.', 'info')
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


@checkout_bp.route('/newsletter', methods=['POST'])
def newsletter():
    email = request.form.get('email')
    if not email:
        flash('Por favor ingresa un correo válido.', 'error')
        return redirect(request.referrer or '/')

    try:
        from app.app import mail
        from flask_mail import Message
        msg = Message(
            "¡Bienvenido al Movimiento AXIS! 🎁 Tu regalo de bienvenida",
            recipients=[email]
        )
        msg.html = render_template(
            'emails/newsletter.html',
            url_host=request.host_url.rstrip('/')
        )
        mail.send(msg)
        flash('¡Gracias por unirte! Revisa tu correo, te hemos enviado un regalo. 🖤', 'success')
    except Exception as e:
        # Fallback si el correo falla, pero el usuario se "suscribió"
        flash('¡Bienvenido al movimiento! (Usa el código AXIS10 para un 10% de descuento)', 'success')
        print(f"Error newsletter mail: {e}")

    return redirect(request.referrer or '/')


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

    import json
    from sqlalchemy import text

    # Generar folio único
    numero_pedido = f"AXIS-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
    uuid_venta = str(uuid.uuid4())

    # Preparar items para el SP
    json_items = []
    for item in cart:
        json_items.append({
            'uuid_producto': item['uuid_producto'],
            'quantity': int(item['quantity']),
            'price': float(item['price'])
        })

    try:
        # ── El SP maneja TODA la lógica de negocio ACID: ──────────────────
        # venta, descuento de stock, pedidos pendientes, órdenes de producción
        # y reserva de materiales (ejecucion_corte + ejecucion_corte_rollo)
        sp_query = text("CALL sp_procesar_venta_hibrida(:u_v, :n_p, :u_c, :m_p, :j_i, @resumen)")
        db.session.execute(sp_query, {
            'u_v': uuid_venta,
            'n_p': numero_pedido,
            'u_c': current_user.cliente.uuid_cliente,
            'm_p': request.form.get('metodo_pago', 'Transferencia'),
            'j_i': json.dumps(json_items)
        })

        # Leer resultado del parametro OUT del SP
        res_row = db.session.execute(text("SELECT @resumen")).fetchone()
        resumen = json.loads(res_row[0]) if res_row and res_row[0] else {}

        db.session.commit()

        # Limpiar carrito y descuentos de sesión
        save_cart([])
        session.pop('axis_discount', None)
        session.pop('discount_code', None)

        if resumen.get('has_pedido'):
            flash("Tu compra incluye prendas que entrarán a producción (+5 días entrega).", 'info')

        flash(f"¡Compra procesada exitosamente! Folio: {numero_pedido}", 'success')
        return redirect(url_for('checkout.pedido_exito', numero_pedido=numero_pedido))

    except Exception as e:
        db.session.rollback()
        import traceback
        logger.error(f">>> [CHECKOUT] ERROR COMPLETO:\n{traceback.format_exc()}")
        flash(f"Error al procesar la compra. Por favor intenta de nuevo.", 'error')
        return redirect(url_for('checkout.checkout_view'))
        

@checkout_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    if not current_user.cliente:
        return redirect(url_for('checkout.completar_perfil'))
    
    ventas = VentaEncabezado.query.filter_by(uuid_cliente=current_user.cliente.uuid_cliente).order_by(VentaEncabezado.fecha_venta.desc()).all()
    pedidos_pendientes = PedidoClienteEncabezado.query.filter_by(uuid_cliente=current_user.cliente.uuid_cliente).order_by(PedidoClienteEncabezado.fecha_pedido.desc()).all()
    
    for v in ventas:
        total = 0
        for d in v.detalles:
            total += (d.precio_unitario_historico * d.cantidad)
        v.total_calculado = total

    for p in pedidos_pendientes:
        total = 0
        for d in p.detalles:
            total += (d.precio_unitario_historico * d.cantidad)
        p.total_calculado = total

    return render_template('mis_pedidos.html', ventas=ventas, pedidos_pendientes=pedidos_pendientes)


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
        
        cliente.telefono = re.sub(r'\D', '', str(telefono))
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
            telefono=re.sub(r'\D', '', str(telefono)),
            direccion_completa=direccion
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash("Perfil guardado. Continuemos con tu compra.", "success")
        return redirect(url_for('checkout.checkout_view'))

    return render_template('completar_perfil.html')