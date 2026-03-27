from flask import redirect, url_for, flash, request
from flask_security import current_user, login_required
from flask_security.confirmable import send_confirmation_instructions
from . import security_bp


@security_bp.before_app_request
def intercept_unconfirmed_login():
    """
    Intercepta el POST de login antes de que Flask-Security lo procese.
    Si el usuario existe pero no ha confirmado su email, reenvía el correo
    y redirige a la pantalla de confirmación automáticamente.
    """
    if request.method == 'POST' and request.path == '/login':
        email = request.form.get('email', '').strip()
        if email:
            from app.models.usuarios import Usuario
            from flask_security.confirmable import send_confirmation_instructions
            user = Usuario.query.filter_by(email=email).first()
            if user and not user.confirmed_at:
                send_confirmation_instructions(user)
                flash('Tu cuenta aún no ha sido verificada. Te hemos reenviado un correo de confirmación.', 'warning')
                return redirect(url_for('security.send_confirmation'))


@security_bp.route('/post-login')
@login_required
def post_login():
    """Redirige al layout correcto según el rol del usuario."""
    user_roles = [role.name for role in current_user.roles]

    if any(role in user_roles for role in ['admin', 'gerente', 'produccion']):
        return redirect(url_for('usuarios.index'))
    elif 'cliente' in user_roles or not user_roles:
        return redirect(url_for('catalog.index'))
    else:
        from flask_security.utils import logout_user
        logout_user()
        flash('Tu cuenta no tiene los permisos necesarios para acceder.', 'error')
        return redirect(url_for('security.login'))


@security_bp.route('/post-register')
def post_register():
    """Muestra la pantalla de 'verifica tu correo' después de registrarse."""
    return redirect(url_for('security.send_confirmation'))
