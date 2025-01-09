from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect, CSRFError

from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    Talisman(
        app,
        force_https=app.config.get("ENV") == "production",
        force_https_permanent=True,
    )

    from app.api import api_blueprint

    app.register_blueprint(api_blueprint)

    CORS(app, supports_credentials=True)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return {"message": "missing or invalid CSRF token"}, 400

    return app
