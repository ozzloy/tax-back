from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect, CSRFError
import json
import os

from config import Config
from app.db import db
from app.model import King, Theme

csrf = CSRFProtect()


def set_default_theme(db, theme_data):
    name = theme_data["name"]

    default_theme = Theme.query.filter_by(
        name=name, king=None
    ).first()

    if default_theme:
        for key, value in theme_data.items():
            setattr(default_theme, key, value)
    else:
        theme_data["king_id"] = None
        default_theme = Theme(**theme_data)
        db.session.add(default_theme)

    db.session.commit()


def init_default_theme(db, app):
    with app.app_context():
        theme_path = os.path.join(app.root_path, "..", "theme.json")
        with open(theme_path, "r") as f:
            theme_data = json.load(f)
            set_default_theme(db, theme_data)


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
        db.create_all()
        init_default_theme(db, app)

    return app
