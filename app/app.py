from flask import Flask
from flask_migrate import Migrate
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.utils.database_connection import db
import app.models  # noqa: F401 — ensures all models are registered with SQLAlchemy


def create_app():
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)
    Migrate(application, db)

    return application


app = create_app()
