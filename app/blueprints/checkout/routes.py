from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_security import login_required, current_user
from app.utils.database_connection import db
from app.models.clientes import Cliente
from app.models.modelos_productos import ProductoTerminado
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
    subtotal = 0
    for item in cart:
        subtotal += float(item.get('price', 0)) * int(item.get('quantity', 1))
    shipping = 9.99 if subtotal < 100 else 0
    total = subtotal + shipping
    return {'subtotal': subtotal, 'shipping': shipping, 'total': total}


@checkout_bp.route('/carrito/agregar', methods=['POST'])
def agregar_carrito():
    uuid_modelo = request.form.get('uuid_producto')  # Del catálogo viene el ID del modelo
    try:
        cantidad = int(request.form.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 1
    talla = request.form.get('talla', 'M')

    if not uuid_modelo:
        flash('Producto no especificado', 'error')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    # Intentar encontrar el producto terminado específico por modelo y talla
    producto = ProductoTerminado.query.filter_by(uuid_modelo=uuid_modelo, talla=talla, active=True).first()
    
    if not producto:
        # Fallback 1: Buscar cualquier talla disponible para ese modelo
        producto = ProductoTerminado.query.filter_by(uuid_modelo=uuid_modelo, active=True).first()
    
    if not producto:
        # Fallback 2: Intentar buscar por ID directo por si acaso
        producto = ProductoTerminado.query.get(uuid_modelo)
    
    if not producto or not producto.active:
        flash('Lo sentimos, este producto no está disponible en este momento.', 'error')
        return redirect(request.referrer or url_for('catalog.catalog_view'))

    stock_disponible = producto.stock_fisico_actual or 0
    if stock_disponible < cantidad:
        flash(f'Solo hay {stock_disponible} unidades disponibles de {producto.modelo.nombre_modelo}', 'warning')
        if stock_disponible <= 0:
            return redirect(request.referrer or url_for('catalog.catalog_view'))
        cantidad = stock_disponible

    cart = load_cart()

    # Buscar si ya existe este producto específico (por su uuid_producto real)
    existing_idx = None
    for idx, item in enumerate(cart):
        if item.get('uuid_producto') == producto.uuid_producto:
            existing_idx = idx
            break

    if existing_idx is not None:
        nueva_cantidad = cart[existing_idx]['quantity'] + cantidad
        if nueva_cantidad > stock_disponible:
            cart[existing_idx]['quantity'] = stock_disponible
            flash(f'Se ajustó la cantidad al máximo disponible ({stock_disponible})', 'info')
        else:
            cart[existing_idx]['quantity'] = nueva_cantidad
    else:
        cart.append({
            'uuid_producto': producto.uuid_producto,
            'uuid_modelo': producto.uuid_modelo,
            'nombre': producto.modelo.nombre_modelo if producto.modelo else 'Producto',
            'talla': producto.talla,
            'price': float(producto.precio_venta),
            'image': producto.modelo.imagen_url if producto.modelo else '/static/images/default/default-image.png',
            'quantity': cantidad,
            'stock': stock_disponible
        })

    save_cart(cart)
    session['open_cart'] = True  # Flag para abrir el carrito en el frontend
    flash(f'¡{producto.modelo.nombre_modelo} añadido al carrito! ✓', 'success')
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

    stock_disponible = producto.stock_fisico_actual or 0
    if cantidad > stock_disponible:
        flash(f'Solo hay {stock_disponible} unidades disponibles', 'error')
        return redirect(url_for('checkout.checkout_view'))

    cart = load_cart()

    if cantidad <= 0:
        # Si cantidad es 0 o negativa, eliminar el item
        cart = [i for i in cart if not (i.get('uuid_producto') == uuid_producto and i.get('talla') == talla)]
    else:
        for idx, item in enumerate(cart):
            if item.get('uuid_producto') == uuid_producto and item.get('talla') == talla:
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
    if not current_user.cliente:
        flash('Por favor completa tu perfil primero', 'error')
        return redirect(url_for('checkout.completar_perfil'))

    cart = load_cart()
    if not cart:
        flash('El carrito está vacío', 'error')
        return redirect(url_for('checkout.checkout_view'))

    try:
        for item in cart:
            producto = ProductoTerminado.query.get(item['uuid_producto'])
            if not producto or not producto.active:
                flash(f'El producto {item["nombre"]} ya no está disponible', 'error')
                return redirect(url_for('checkout.checkout_view'))

            stock_disponible = producto.stock_fisico_actual or 0
            if stock_disponible < item['quantity']:
                flash(f'No hay suficiente stock de {item["nombre"]}. Disponible: {stock_disponible}', 'error')
                return redirect(url_for('checkout.checkout_view'))

        numero_pedido = f"AXIS-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

        venta = VentaEncabezado(
            uuid_venta=str(uuid.uuid4()),
            numero_pedido=numero_pedido,
            uuid_cliente=current_user.cliente.uuid_cliente,
            metodo_pago=request.form.get('metodo_pago', 'Transferencia'),
            estatus_envio='Procesando'
        )
        db.session.add(venta)
        db.session.flush()

        for item in cart:
            producto = ProductoTerminado.query.get(item['uuid_producto'])

            detalle = VentaDetalle(
                uuid_detalle=str(uuid.uuid4()),
                uuid_venta=venta.uuid_venta,
                uuid_producto=item['uuid_producto'],
                cantidad=item['quantity'],
                precio_unitario_historico=Decimal(str(item['price']))
            )
            db.session.add(detalle)
            producto.stock_fisico_actual -= item['quantity']

        db.session.commit()

        # Limpiar carrito de la sesión
        save_cart([])

        flash(f'¡Pedido realizado! Número: {numero_pedido}', 'success')
        return redirect(url_for('checkout.pedido_exito', numero_pedido=numero_pedido))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al procesar el pedido: {str(e)}', 'error')
        return redirect(url_for('checkout.checkout_view'))


@checkout_bp.route('/checkout/exito/<numero_pedido>')
@login_required
def pedido_exito(numero_pedido):
    return render_template('pedido_exito.html', numero_pedido=numero_pedido)


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