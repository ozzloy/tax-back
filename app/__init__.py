"""create the flask app for tax backend."""

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFError, CSRFProtect
from http import HTTPStatus as http
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import Config
from app.db import db
from app.seed import seed


csrf = CSRFProtect()


def create_app(config_class=Config):
    """Create the flask app for tax."""
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
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
        return {
            "message": "missing or invalid CSRF token"
        }, http.FORBIDDEN

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return {
            "message": "validation error",
            "errors": {
                err["loc"][0]: err["msg"] for err in e.errors()
            },
        }, http.UNPROCESSABLE_ENTITY

    @app.errorhandler(IntegrityError)
    def handle_db_error(e):
        db.session.rollback()
        field = "email" if "email" in str(e.orig) else "nick"

        return {
            "message": "account conflict",
            "errors": {field: f"{field} is taken"},
        }, http.CONFLICT

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        print(f"error type: {type(e).__name__}")
        print(f"error message: {str(e)}")

        import traceback

        print("\ntraceback:")
        print(traceback.format_exc())

        return {"error": str(e)}, http.INTERNAL_SERVER_ERROR

    with app.app_context():
        ensure_schema_sql = text(
            "CREATE SCHEMA IF NOT EXISTS " + config_class.DB_SCHEMA
        )
        db.drop_all()
        db.session.execute(ensure_schema_sql)
        db.session.commit()
        db.create_all()
        seed()

    return app
