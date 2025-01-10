from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect, CSRFError
import json
import os
from sqlalchemy import text

from config import Config
from app.db import db
from app.model import King, Theme
from app.seed import seed


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

    with app.app_context():
        ensure_schema_sql = text(
            "CREATE SCHEMA IF NOT EXISTS " + config_class.DB_SCHEMA
        )
        db.session.execute(ensure_schema_sql)
        db.session.commit()
        db.create_all()
        seed()

    return app
