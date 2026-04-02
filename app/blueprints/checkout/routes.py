from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from app.utils.database_connection import db
from app.models.clientes import Cliente

checkout_bp = Blueprint('checkout', __name__, template_folder='../../templates/client')

@checkout_bp.route('/checkout')
@login_required
def checkout_view():
    if not current_user.cliente_profile:
        # Interceptor: Redirigir a recabar los datos operativos del cliente antes de permitir carrito
        return redirect(url_for('checkout.completar_perfil'))
    return render_template('carrito.html')

@checkout_bp.route('/checkout/completar_perfil', methods=['GET', 'POST'])
@login_required
def completar_perfil():
    if current_user.cliente_profile:
        return redirect(url_for('checkout.checkout_view'))

    if request.method == 'POST':
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion_completa')

        if not telefono or len(direccion) < 5:
            flash("Por favor proporcione un teléfono y una dirección válida.", "error")
            return render_template('completar_perfil.html')

        nuevo_cliente = Cliente(
            uuid_usuario=current_user.uuid_usuario,
            telefono=telefono,
            direccion_completa=direccion
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash("Perfil guardado. Continuemos con tu pago.", "success")
        return redirect(url_for('checkout.checkout_view'))

    return render_template('completar_perfil.html')
