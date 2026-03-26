from flask import redirect, url_for
from flask_security import current_user, login_required
from . import security_bp


@security_bp.route('/post-login')
@login_required
def post_login():
    """Redirige al layout correcto según el rol del usuario."""
    user_roles = [role.name for role in current_user.roles]

    if any(role in user_roles for role in ['admin', 'gerente', 'produccion']):
        return redirect(url_for('usuarios.index'))
    elif 'cliente' in user_roles:
        return redirect('/client')
    else:
        # Rol no reconocido — redirigir a login
        return redirect(url_for('security.login'))


@security_bp.route('/post-register')
def post_register():
    """Muestra la pantalla de 'verifica tu correo' después de registrarse."""
    return redirect(url_for('security.send_confirmation'))
