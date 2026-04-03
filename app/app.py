import os
from dotenv import load_dotenv
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
    #
    load_dotenv()
    #
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
    application.config['SECURITY_LOGIN_WITHOUT_CONFIRMATION'] = False
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
    application.config['SECURITY_MSG_CONFIRMATION_REQUIRED'] = (
        'Tu cuenta no ha sido verificada. <a href="/confirm">Haz clic aquí para reenviar el correo de confirmación.</a>',
        'error'
    )
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
    application.config['SECURITY_POST_REGISTER_VIEW'] = '/confirm'
    application.config['SECURITY_POST_CONFIRM_VIEW'] = '/login'
    application.config['SECURITY_LOGIN_URL'] = '/login'
    application.config['SECURITY_LOGOUT_URL'] = '/logout'
    application.config['SECURITY_REGISTER_URL'] = '/register'
    application.config['SECURITY_AUTO_LOGIN_AFTER_CONFIRM'] = False
    application.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = '7 days'

    # No redirigir a /login automáticamente si no está autenticado (usamos nuestra lógica)
    application.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'

    # Forzar que Flask genere URLs con localhost:3030 (no la IP interna de Docker)
    application.config['SERVER_NAME'] = os.getenv('SERVER_NAME', 'localhost:3030')

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

    # ── Debug: log confirmation & login events ────────────────
    from flask_security import user_confirmed, user_authenticated
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('axis_security')

    @user_confirmed.connect_via(application)
    def on_user_confirmed(sender, user, **kwargs):
        logger.info(f'[CONFIRM] Email confirmado para: {user.email} | confirmed_at={user.confirmed_at}')

    @user_authenticated.connect_via(application)
    def on_user_authenticated(sender, user, **kwargs):
        logger.info(f'[LOGIN] Login exitoso para: {user.email} | confirmed_at={user.confirmed_at}')

    @application.before_request
    def ensure_roles():
        """Asegura que los roles básicos existan en la base de datos."""
        # Esta es una forma rápida de inicializar roles si no existen
        if not Role.query.first():
            roles = ['admin', 'gerente', 'produccion', 'cliente']
            for r in roles:
                user_datastore.create_role(name=r)
            db.session.commit()

    from flask_security import user_registered
    from flask_security.confirmable import send_confirmation_instructions
    from flask import session

    @user_registered.connect_via(application)
    def on_user_registered(sender, user, **kwargs):
        """Asigna el rol 'cliente' automáticamente a cualquier usuario registrado."""
        cliente_role = Role.query.filter_by(name='cliente').first()
        if cliente_role:
            user_datastore.add_role_to_user(user, cliente_role)
            db.session.commit()
            logger.info(f'[REGISTER] Rol "cliente" asignado a: {user.email}')

    # ── Blueprints ────────────────────────────────────────────
    application.register_blueprint(bp.usuarios_bp, url_prefix='/usuarios')
    application.register_blueprint(bp.insumos_bp, url_prefix='/insumos')
    application.register_blueprint(bp.inventario_bp, url_prefix='/inventario')
    application.register_blueprint(bp.compras_bp, url_prefix='/compras')
    application.register_blueprint(bp.categorias_bp, url_prefix='/categorias')
    application.register_blueprint(bp.recetas_bp, url_prefix='/recetas')
    application.register_blueprint(bp.modelos_bp, url_prefix='/modelos')
    application.register_blueprint(bp.productos_bp, url_prefix='/productos_terminados')
    application.register_blueprint(bp.orden_bp, url_prefix='/orden_produccion')
    application.register_blueprint(bp.security_bp, url_prefix='/security')
    application.register_blueprint(bp.catalog_bp, url_prefix='')
    application.register_blueprint(bp.productos_bp, url_prefix='')
    application.register_blueprint(bp.checkout_bp, url_prefix='')
    application.register_blueprint(bp.costo_utilidad_bp, url_prefix='')

    # ── Context Processor for Dynamic Layout ──────────────────
    @application.context_processor
    def inject_layout():
        if current_user.is_authenticated:
            if current_user.has_role('cliente'):
                return {'base_layout': 'client/layout.html'}
            elif any(current_user.has_role(r) for r in ['admin', 'produccion', 'gerente']):
                return {'base_layout': 'produccion/layout.html'}
        return {'base_layout': 'client/layout.html'}

    # ── Catálogo (Ruta Raíz) ──────────────────────────────────
    # Ya está manejado por client_bp con url_prefix=''

    # ── Debug: verificar estado de usuario (QUITAR EN PRODUCCIÓN) ──
    @application.route('/debug/check-user/<email>')
    def debug_check_user(email):
        user = Usuario.query.filter_by(email=email).first()
        if not user:
            return f'Usuario {email} no encontrado', 404
        return (
            f'Email: {user.email}<br>'
            f'confirmed_at: {user.confirmed_at}<br>'
            f'active: {user.active}<br>'
            f'tf_primary_method: {user.tf_primary_method}<br>'
            f'roles: {[r.name for r in user.roles]}'
        )

    # ── Debug: VERIFICAR POR QUÉ FALLA EL TOKEN ──
    @application.route('/debug/test-token/<token>')
    def debug_test_token(token):
        from itsdangerous import URLSafeTimedSerializer
        from itsdangerous.exc import BadSignature, SignatureExpired
        import time

        serializer = URLSafeTimedSerializer(
            application.config['SECRET_KEY'],
            salt=application.config['SECURITY_PASSWORD_SALT']
        )
        try:
            # We use 'confirm' salt which is standard for Flask-Security
            data = serializer.loads(token, salt='confirm-email', max_age=application.config.get('SECURITY_CONFIRM_EMAIL_WITHIN', 86400 * 7))
            return f"TOKEN VÁLIDO. Apunta al usuario_id o data: {data}"
        except SignatureExpired as e:
            return f"TOKEN EXPIRADO: {e}", 400
        except BadSignature as e:
            return f"FIRMA INVÁLIDA (SECRET_KEY o PASSWORD_SALT diferente): {e}", 400
        except Exception as e:
            return f"OTRO ERROR: {e}", 400

    return application
    #

app = create_app()
