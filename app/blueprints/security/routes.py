from flask import redirect, url_for, flash
from flask_security import current_user, login_required
from flask_security.confirmable import send_confirmation_instructions
from . import security_bp


@security_bp.route('/post-login')
@login_required
def post_login():
    """Redirige al layout correcto según el rol del usuario."""

    # Si el usuario no ha confirmado su email, reenviar correo y redirigir
    if not current_user.confirmed_at:
        send_confirmation_instructions(current_user)
        from flask_security.utils import logout_user
        logout_user()
        flash('Tu cuenta aún no ha sido verificada. Te hemos enviado un nuevo correo de confirmación.', 'warning')
        return redirect(url_for('security.send_confirmation'))

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
