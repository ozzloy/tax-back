"""endpoints for kings."""

from flask import Blueprint, request
from http import HTTPStatus as http

from app import db
from app.model import King
from app.schema import KingSignupSchema

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    """Create a new king, aka account."""
    king_signup_data = KingSignupSchema.model_validate(request.json)

    clean_king_data = king_signup_data.model_dump()
    king = King(**clean_king_data, theme_id=1)
    db.session.add(king)
    db.session.commit()
    return {"king": {str(king.id): king.to_dict()}}, http.CREATED
