"""endpoints for kings."""

from flask import Blueprint, request
from http import HTTPStatus as http

from app import db
from app.model import King
from app.schema import KingSignupSchema, StateSchema

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    """Create a new king, aka account."""
    king = KingSignupSchema.model_validate(request.json).model_dump(
        exclude_none=True
    )
    king["theme_id"] = 1

    king = King(**king)

    db.session.add(king)
    db.session.commit()

    state_data = {"king": {str(king.id): king.to_dict()}}
    state = StateSchema.model_validate(state_data).model_dump(
        exclude_none=True
    )

    return state, http.CREATED
