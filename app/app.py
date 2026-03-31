from flask import Flask
from flask_migrate import Migrate
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.utils.database_connection import db
import app.models  # noqa: F401 — ensures all models are registered with SQLAlchemy
from app.blueprints.insumos import insumos_bp
from app.blueprints.categorias import categorias_bp
from app.blueprints.compras import compras_bp
from app.blueprints.inventario import inventario_bp
#

import os
from dotenv import load_dotenv
#


def create_app():
    #
    load_dotenv()
    #
    application = Flask(__name__)

    #
    application.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    #
    
    application.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)
    Migrate(application, db)

    #INSUMOS
    application.register_blueprint(insumos_bp)
    application.register_blueprint(categorias_bp)
    application.register_blueprint(compras_bp)
    application.register_blueprint(inventario_bp)
    return application
    #

app = create_app()
