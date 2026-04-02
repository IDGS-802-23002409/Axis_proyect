from flask import Blueprint, render_template

checkout_bp = Blueprint('checkout', __name__, template_folder='../../templates/client')

@checkout_bp.route('/checkout')
def checkout_view():
    return render_template('carrito.html')
