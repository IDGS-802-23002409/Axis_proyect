from flask import Flask
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.utils.database_connection import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db) 

    # Registro del módulo Proveedores
    from app.blueprints.proveedores.routes import proveedores_bp
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')

    return app
