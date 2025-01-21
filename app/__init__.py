"""create the flask app for tax backend."""

from flask import Flask, request
from flask_cors import CORS
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFError, CSRFProtect
from http import HTTPStatus as http
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from config import Config
from app.db import db
from app.seed import seed
from app.model import King


csrf = CSRFProtect()

debug = False


def create_app(config_class=Config):
    """Create the flask app for tax."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
        app,
        supports_credentials=True,
    )

    login_manager = LoginManager()
    login_manager.init_app(app)

    db.init_app(app)
    csrf.init_app(app)

    Talisman(
        app,
        force_https=app.config.get("ENV") == "production",
        force_https_permanent=True,
    )

    @login_manager.user_loader
    def load_user(king_id):
        return db.session.get(King, int(king_id))

    from app.api import api_blueprint

    app.register_blueprint(api_blueprint)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        if debug:
            print(__file__)
            print(f"403 error on {request.url}")
            print(
                f"request body: {request.get_data().decode('utf-8')}"
            )
            print(f"headers: {dict(request.headers)}")
            import traceback

            print()
            print("e")
            print("\ntraceback:")
            print(traceback.format_exc())
        return {
            "message": "missing or invalid CSRF token"
        }, http.FORBIDDEN

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        if debug:
            import traceback

            print()
            print(__file__)
            print("e")
            print(e)
            print("\ntraceback:")
            print(traceback.format_exc())
            exit(-1)

        errors = {err["loc"][0]: err["msg"] for err in e.errors()}

        if debug:
            from pprint import pprint

            print()
            print(__file__)
            print("errors:")
            pprint(errors)

        return {
            "message": "validation error",
            "errors": errors,
        }, http.UNPROCESSABLE_ENTITY

    @app.errorhandler(IntegrityError)
    def handle_db_error(e):
        db.session.rollback()
        field = "email" if "email" in str(e.orig) else "nick"

        return {
            "message": "account conflict",
            "errors": {field: f"{field} is taken"},
        }, http.CONFLICT

    @app.errorhandler(Unauthorized)
    def handle_unauthorized_error(e):
        return str(e), http.UNAUTHORIZED

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        if debug:
            print()
            print(__file__)
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
