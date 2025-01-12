"""endpoints for kings."""

from flask import Blueprint, request
from flask_login import current_user as current_king, login_required
from http import HTTPStatus as http

from app import db
from app.model import King
from app.schema import KingSignupSchema, StateSchema

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    """Create a new king, aka create new account, aka signup."""
    king = KingSignupSchema.model_validate(request.json).model_dump()
    king["theme_id"] = 1

    king = King(**king)

    db.session.add(king)
    db.session.commit()

    state_data = {
        "current_king_id": None,
        "king": {str(king.id): king.to_dict()},
    }
    state = StateSchema.model_validate(state_data).model_dump()

    return state, http.CREATED


@king_blueprint.route("/", methods=["GET"])
@login_required
def read():
    """Look up info on currently logged in king."""
    king = db.session.get(King, current_king.id).to_private_dict()

    king_id = current_king.id
    state_data = {
        "current_king_id": king_id,
        "king": {str(king_id): king},
    }
    state = StateSchema(**state_data).model_dump()
    return state, http.OK
