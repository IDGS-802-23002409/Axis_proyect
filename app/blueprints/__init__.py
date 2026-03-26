from flask import Flask
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.utils.database_connection import db
from flask_migrate import Migrate
from .usuarios import usuarios_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db) 

    # Registro del módulo Proveedores
    from app.blueprints.proveedores.routes import proveedores_bp
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
    from app.blueprints.usuarios.routes import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app
