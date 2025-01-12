"""login and logout."""

from flask import Blueprint, request
from flask_login import (
    login_user as login_king,
    logout_user as logout_king,
)
from http import HTTPStatus as http

from app.model import King
from app.schema import SessionLoginSchema, StateSchema

session_blueprint = Blueprint(
    "session", __name__, url_prefix="/session"
)


@session_blueprint.route("/", methods=["POST"])
def login():
    """Log in a king."""
    login = SessionLoginSchema.model_validate(
        request.json
    ).model_dump()

    king = King.query.filter(King.email == login["email"]).first()

    if not king or not king.check_password(login["password"]):
        return {"message": "invalid credentials"}, http.UNAUTHORIZED

    login_king(king)

    king_id = str(king.id)
    state = {
        "current_king_id": king_id,
        "king": {king_id: king.to_private_dict()},
    }
    state = StateSchema.model_validate(state).model_dump(
        exclude_none=True
    )
    return state, http.OK


@session_blueprint.route("/", methods=["DELETE"])
def logout():
    """Log out the current king."""
    logout_king()
    return "", http.NO_CONTENT
