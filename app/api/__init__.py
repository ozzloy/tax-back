from flask import Blueprint

from .king_routes import king_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(king_blueprint)
