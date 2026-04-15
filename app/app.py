import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from app.blueprints.security.forms import ExtendedRegisterForm
from app.utils.config import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME,
    ADMIN_DB_USER, ADMIN_DB_PASSWORD,
    GERENTE_DB_USER, GERENTE_DB_PASSWORD,
    PRODUCCION_DB_USER, PRODUCCION_DB_PASSWORD,
    CLIENTE_DB_USER, CLIENTE_DB_PASSWORD,
    BACKUP_DB_USER, BACKUP_DB_PASSWORD,
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER, SECURITY_TOTP_SECRETS
)
from app.utils.database_connection import db
import app.models  # noqa: F401 — ensures all models are registered with SQLAlchemy
from app.models.usuarios import Usuario, Role
import app.blueprints as bp
from app.blueprints import dashboard_administrativo
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
    application.jinja_env.add_extension('jinja2.ext.do')
    application.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    application.config['SQLALCHEMY_BINDS'] = {
        'admin_rol': f"mysql+pymysql://{ADMIN_DB_USER}:{ADMIN_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        'gerente_rol': f"mysql+pymysql://{GERENTE_DB_USER}:{GERENTE_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        'produccion_rol': f"mysql+pymysql://{PRODUCCION_DB_USER}:{PRODUCCION_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        'cliente_rol': f"mysql+pymysql://{CLIENTE_DB_USER}:{CLIENTE_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        'backup_rol': f"mysql+pymysql://{BACKUP_DB_USER}:{BACKUP_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    }
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
    # application.config['SECURITY_TWO_FACTOR'] = True
    application.config['SECURITY_TWO_FACTOR'] = False
    application.config['SECURITY_TWO_FACTOR_REQUIRED'] = False
    # application.config['SECURITY_TWO_FACTOR_REQUIRED'] = True
    application.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['email', 'authenticator']
    application.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = True
    application.config['SECURITY_TOTP_SECRETS'] = {
        '1': SECURITY_TOTP_SECRETS
    }
    application.config['SECURITY_TOTP_ISSUER'] = 'Axis Urban Apparel'

    # Seguridad avanzada: Códigos de recuperación y Sesiones
    application.config['SECURITY_MULTI_FACTOR_RECOVERY_CODES'] = True
    application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    application.config['SESSION_REFRESH_EACH_REQUEST'] = True

    # Plantillas personalizadas
    application.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'
    application.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'security/register_user.html'
    application.config['SECURITY_SEND_CONFIRMATION_TEMPLATE'] = 'security/send_confirmation.html'
    application.config['SECURITY_RESET_PASSWORD_TEMPLATE'] = 'security/reset_password.html'
    application.config['SECURITY_FORGOT_PASSWORD_TEMPLATE'] = 'security/reset_password.html'
    application.config['SECURITY_TWO_FACTOR_SETUP_TEMPLATE'] = 'security/two_factor_setup.html'
    application.config['SECURITY_TWO_FACTOR_VERIFY_CODE_TEMPLATE'] = 'security/two_factor_verify_code.html'
    application.config['SECURITY_TWO_FACTOR_RESCUE_TEMPLATE'] = 'security/two_factor_rescue.html'

    # Redirecciones
    application.config['SECURITY_POST_LOGIN_VIEW'] = '/security/post-login'
    application.config['SECURITY_POST_LOGOUT_VIEW'] = '/'
    application.config['SECURITY_POST_REGISTER_VIEW'] = '/confirm'
    application.config['SECURITY_POST_CONFIRM_VIEW'] = '/login'
    application.config['SECURITY_LOGIN_URL'] = '/login'
    application.config['SECURITY_LOGOUT_URL'] = '/logout'
    application.config['SECURITY_REGISTER_URL'] = '/register'
    application.config['SECURITY_AUTO_LOGIN_AFTER_CONFIRM'] = False
    application.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = '7 days'

    # Redirigir a la tienda si el usuario no tiene permisos suficientes
    application.config['SECURITY_UNAUTHORIZED_VIEW'] = '/'

    # Forzar que Flask genere URLs con localhost:3030 (no la IP interna de Docker)
    # application.config['SERVER_NAME'] = os.getenv('SERVER_NAME', 'localhost:3030')

    # ── Init extensions ───────────────────────────────────────
    csrf.init_app(application)
    db.init_app(application)
    mail.init_app(application)
    Migrate(application, db)

    from app.utils.audit_listeners import register_audit_listeners
    register_audit_listeners()

    from app.utils.backup_commands import init_backup_cli
    init_backup_cli(application)

    from app.utils.db_hooks import init_db_objects
    init_db_objects(application)

    from app.blueprints.dashboard_administrativo import dashboard_bp
    application.register_blueprint(dashboard_bp, url_prefix='/dashboard_administrativo')

    from app.blueprints.proveedores import proveedores_bp
    application.register_blueprint(proveedores_bp, url_prefix='/proveedores')

    from app.blueprints.alertas import alertas_bp
    application.register_blueprint(alertas_bp, url_prefix='/alertas')

    from app.blueprints.ventas import ventas_bp
    application.register_blueprint(ventas_bp, url_prefix='/ventas')

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

    from flask_login import user_logged_out
    from flask import session
    
    @user_logged_out.connect_via(application)
    def on_user_logged_out(sender, user, **kwargs):
        if 'axis_cart' in session:
            session.pop('axis_cart')
        logger.info(f'[LOGOUT] Sesión cerrada y carrito vaciado para: {user.email}')

    from flask import g
    @application.before_request
    def set_db_role_g():
        """Mapea el rol de Flask-Security al rol de base de datos en g.db_role."""
        if current_user.is_authenticated:
            if current_user.has_role('admin'):
                g.db_role = 'admin_rol'
            elif current_user.has_role('gerente'):
                g.db_role = 'gerente_rol'
            elif current_user.has_role('produccion'):
                g.db_role = 'produccion_rol'
            else:
                g.db_role = 'cliente_rol'
        else:
            # Usuarios anónimos usan el rol de cliente (público)
            g.db_role = 'cliente_rol'

    @application.before_request
    def set_db_bind():
        """Cambia el engine de la sesión según el rol en g.db_role."""
        if hasattr(g, 'db_role'):
            # Lista de roles que tienen su propio bind (ahora todos)
            roles_with_binds = ['admin_rol', 'gerente_rol', 'produccion_rol', 'cliente_rol', 'backup_rol']
            
            if g.db_role in roles_with_binds:
                # Cambiamos el engine de la sesión para este request
                engine = application.extensions['sqlalchemy'].get_engine(bind=g.db_role)
                db.session.bind = engine
            else:
                # Volver al default (flask_user con ALL PRIVILEGES)
                engine = application.extensions['sqlalchemy'].get_engine()
                db.session.bind = engine
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
    # El catálogo debe ir de los primeros con prefix='' para evitar shadowing
    application.register_blueprint(bp.catalog_bp, url_prefix='')
    application.register_blueprint(bp.checkout_bp, url_prefix='')
    application.register_blueprint(bp.costo_utilidad_bp, url_prefix='')

    application.register_blueprint(bp.usuarios_bp, url_prefix='/usuarios')
    application.register_blueprint(bp.empleados_bp, url_prefix='/empleados')
    application.register_blueprint(bp.clientes_bp, url_prefix='/clientes')
    application.register_blueprint(bp.insumos_bp, url_prefix='/insumos')
    application.register_blueprint(bp.inventario_bp, url_prefix='/inventario')
    application.register_blueprint(bp.compras_bp, url_prefix='/compras')
    application.register_blueprint(bp.categorias_bp, url_prefix='/categorias')
    application.register_blueprint(bp.recetas_bp, url_prefix='/recetas')
    application.register_blueprint(bp.pedidos_proveedor_bp, url_prefix='/pedidos_proveedor')
    application.register_blueprint(bp.productos_bp, url_prefix='/productos_terminados')
    application.register_blueprint(bp.orden_bp, url_prefix='/orden_produccion')
    application.register_blueprint(bp.security_bp, url_prefix='/security')
    application.register_blueprint(bp.merma_bp, url_prefix='/merma')
    application.register_blueprint(bp.respaldos_bp, url_prefix='/respaldos')

    # ── CSRF Exemptions (rutas públicas del carrito) ──────────────
    # El carrito es una función pública del ecommerce: cualquier usuario
    # (autenticado o no) debe poder agregar/quitar productos.
    # Solo procesar_checkout (que crea la orden) mantiene CSRF.
    from app.blueprints.checkout.routes import (
        agregar_carrito, actualizar_carrito, eliminar_carrito, vaciar_carrito
    )
    csrf.exempt(agregar_carrito)
    csrf.exempt(actualizar_carrito)
    csrf.exempt(eliminar_carrito)
    csrf.exempt(vaciar_carrito)

    # ── Context Processor for Dynamic Layout ──────────────────
    @application.context_processor
    def inject_layout():
        if current_user.is_authenticated:
            if current_user.has_role('cliente'):
                return {'base_layout': 'client/base.html'}
            elif any(current_user.has_role(r) for r in ['admin', 'produccion', 'gerente']):
                return {'base_layout': 'produccion/layout.html'}
        # Usuarios no autenticados y clientes públicos -> layout cliente
        return {'base_layout': 'client/base.html'}

    # ── Context Processor for Cart (JSON file) ──────────────────
    @application.context_processor
    def inject_cart():
        try:
            from app.blueprints.checkout.routes import load_cart
            cart = load_cart()
            total_items = sum(item.get('quantity', 0) for item in cart)
            return {'cart_items': cart, 'cart_count': total_items}
        except Exception:
            pass
        return {'cart_items': [], 'cart_count': 0}

    # ── Timezone Adjustment Filter ────────────────────────────
    @application.template_filter('timezone_adjust')
    def timezone_adjust(dt, offset=-6):
        if dt is None:
            return None
        from datetime import timedelta
        return dt + timedelta(hours=offset)

    # ── Prevent Cache on Protected Routes ─────────────────────
    @application.after_request
    def add_header(response):
        """
        Añade encabezados para evitar que el navegador guarde en caché
        páginas sensibles. Si el usuario cierra sesión y presiona 'atrás',
        no verá la información anterior.
        """
        if current_user.is_authenticated:
            session.permanent = True
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

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

    # ── Global Error Handlers ─────────────────────────────────
    from flask import render_template as rt

    @application.errorhandler(400)
    def bad_request(e):
        return rt('client/error.html',
                  code=400,
                  title='Solicitud Inválida',
                  message='Algo salió mal con tu solicitud. Puede ser un problema de sesión. Intenta recargar la página o regresar al inicio.'), 400

    @application.errorhandler(403)
    def forbidden(e):
        from flask import flash
        flash("No tienes permisos para acceder a esta sección. Hemos vuelto al catálogo.", "warning")
        return redirect('/')

    @application.errorhandler(404)
    def not_found(e):
        return rt('client/error.html',
                  code=404,
                  title='Página No Encontrada',
                  message='La página que buscas no existe o fue movida. Explora nuestro catálogo o regresa al inicio.'), 404

    @application.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return rt('client/error.html',
                  code=500,
                  title='Error Interno',
                  message='Algo salió mal en nuestro servidor. Ya estamos trabajando en ello. Por favor intenta de nuevo más tarde.'), 500

    return application
    #

app = create_app()
