import os

from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from app.blueprints.security.forms import ExtendedRegisterForm
from app.utils.config import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME,
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER, SECURITY_TOTP_SECRETS
)
from app.utils.database_connection import db
import app.models  # noqa: F401 — ensures all models are registered with SQLAlchemy
from app.models.usuarios import Usuario, Role
import app.blueprints as bp
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
mail = Mail()


def create_app():
    application = Flask(__name__)

    # ── Core ──────────────────────────────────────────────────
    application.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')
    application.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── Mail ──────────────────────────────────────────────────
    application.config['MAIL_SERVER'] = MAIL_SERVER
    application.config['MAIL_PORT'] = MAIL_PORT
    application.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    application.config['MAIL_USERNAME'] = MAIL_USERNAME
    application.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    application.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

    # ── Flask-Security ────────────────────────────────────────
    application.config['SECURITY_PASSWORD_SALT'] = os.getenv(
        'SECURITY_PASSWORD_SALT', 'change-me-salt'
    )
    application.config['SECURITY_REGISTERABLE'] = True
    application.config['SECURITY_CONFIRMABLE'] = True
    application.config['SECURITY_RECOVERABLE'] = True
    application.config['SECURITY_CHANGEABLE'] = True
    application.config['SECURITY_SEND_REGISTER_EMAIL'] = True
    application.config['SECURITY_PASSWORD_HASH'] = 'argon2'
    application.config['SECURITY_PASSWORD_SCHEMES'] = ['argon2']

    # Validación de contraseña
    application.config['SECURITY_PASSWORD_LENGTH_MIN'] = 8

    # Mensajes de error en español
    application.config['SECURITY_MSG_INVALID_PASSWORD'] = ('Contraseña inválida.', 'error')
    application.config['SECURITY_MSG_PASSWORD_NOT_SET'] = ('No se ha establecido una contraseña.', 'error')
    application.config['SECURITY_MSG_USER_DOES_NOT_EXIST'] = ('El usuario no existe.', 'error')
    application.config['SECURITY_MSG_INVALID_EMAIL_ADDRESS'] = ('Dirección de email inválida.', 'error')
    application.config['SECURITY_MSG_CONFIRMATION_REQUIRED'] = ('Debes confirmar tu email antes de iniciar sesión.', 'error')
    application.config['SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED'] = ('Este email ya está registrado.', 'error')
    application.config['SECURITY_MSG_PASSWORD_MISMATCH'] = ('Las contraseñas no coinciden.', 'error')
    application.config['SECURITY_MSG_EMAIL_NOT_PROVIDED'] = ('Debes proporcionar un email.', 'error')
    application.config['SECURITY_MSG_PASSWORD_INVALID_LENGTH'] = ('La contraseña debe tener al menos 8 caracteres.', 'error')
    application.config['SECURITY_MSG_TWO_FACTOR_INVALID_TOKEN'] = ('Código de verificación inválido.', 'error')

    # 2FA — solo email y authenticator, sin SMS
    application.config['SECURITY_TWO_FACTOR'] = True
    application.config['SECURITY_TWO_FACTOR_REQUIRED'] = True
    application.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['email', 'authenticator']
    application.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = True
    application.config['SECURITY_TOTP_SECRETS'] = {
        '1': SECURITY_TOTP_SECRETS
    }
    application.config['SECURITY_TOTP_ISSUER'] = 'Axis Urban Apparel'

    # Plantillas personalizadas
    application.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'
    application.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'security/register_user.html'
    application.config['SECURITY_SEND_CONFIRMATION_TEMPLATE'] = 'security/send_confirmation.html'
    application.config['SECURITY_RESET_PASSWORD_TEMPLATE'] = 'security/reset_password.html'
    application.config['SECURITY_FORGOT_PASSWORD_TEMPLATE'] = 'security/reset_password.html'
    application.config['SECURITY_TWO_FACTOR_SETUP_TEMPLATE'] = 'security/two_factor_setup.html'
    application.config['SECURITY_TWO_FACTOR_VERIFY_CODE_TEMPLATE'] = 'security/two_factor_verify_code.html'

    # Redirecciones
    application.config['SECURITY_POST_LOGIN_VIEW'] = '/security/post-login'
    application.config['SECURITY_POST_REGISTER_VIEW'] = '/security/post-register'
    application.config['SECURITY_POST_CONFIRM_VIEW'] = '/login'
    application.config['SECURITY_LOGIN_URL'] = '/login'
    application.config['SECURITY_LOGOUT_URL'] = '/logout'
    application.config['SECURITY_REGISTER_URL'] = '/register'

    # No redirigir a /login automáticamente si no está autenticado (usamos nuestra lógica)
    application.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'

    # ── Init extensions ───────────────────────────────────────
    csrf.init_app(application)
    db.init_app(application)
    mail.init_app(application)
    Migrate(application, db)

    # Flask-Security datastore
    user_datastore = SQLAlchemyUserDatastore(db, Usuario, Role)
    security = Security(
        application,
        user_datastore,
        confirm_register_form=ExtendedRegisterForm
    )

    # ── Blueprints ────────────────────────────────────────────
    application.register_blueprint(bp.usuarios_bp)
    application.register_blueprint(bp.security_bp, url_prefix='/security')

    # ── Ruta raíz → login ─────────────────────────────────────
    @application.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('security_bp.post_login'))
        return redirect(url_for('security.login'))

    return application


app = create_app()
