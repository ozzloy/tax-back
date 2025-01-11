"""all the routes for the api."""

from flask import Blueprint
from flask_wtf.csrf import generate_csrf

from .king_route import king_blueprint
from .session_route import session_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/csrf-token")
def get_csrf_token():
    """Generate and return csrf token."""
    return {"csrf_token": generate_csrf()}


api_blueprint.register_blueprint(king_blueprint)
api_blueprint.register_blueprint(session_blueprint)
