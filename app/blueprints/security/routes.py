from flask import render_template
from . import security_bp

@security_bp.route('/login-preview')
def login_preview():
    return render_template('login.html')

@security_bp.route('/register-preview')
def register_preview():
    return render_template('register_user.html')

@security_bp.route('/2fa-setup-preview')
def two_factor_setup_preview():
    return render_template('two_factor_setup.html')

@security_bp.route('/2fa-auth-preview')
def two_factor_authenticate_preview():
    return render_template('two_factor_authenticate.html')
