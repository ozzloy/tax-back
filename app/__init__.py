from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    Talisman(
        app,
        force_https=app.config.get("ENV") == "production",
        force_https_permanent=True,
    )

    from app.api import api_blueprint

    app.register_blueprint(api_blueprint)

    CORS(app)

    return app
