"""login and logout."""

from flask import Blueprint, request
from flask_login import login_user as login_king
from http import HTTPStatus as http

from app.model import King
from app.schema import SessionLoginSchema

session_blueprint = Blueprint(
    "session", __name__, url_prefix="/session"
)


@session_blueprint.route("/", methods=["POST"])
def login():
    """Log in a king."""
    login = SessionLoginSchema.model_validate(request.json)

    king = King.query.filter(King.email == login["email"]).first()

    if not king or not king.check_password(login["password"]):
        return {"message": "invalid credentials"}, http.UNAUTHORIZED

    login_king(king)

    return {"current_king": {str(king.id): king.to_dict()}}
