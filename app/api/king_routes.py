"""endpoints for kings."""

from flask import Blueprint, request
from http import HTTPStatus as http
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from app import db
from app.model import King
from app.schema import KingSignupSchema

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    """Create a new king, aka account."""
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")

    try:
        king_signup_data = KingSignupSchema.model_validate(
            request.json
        )

        clean_king_data = king_signup_data.model_dump()
        king = King(**clean_king_data, theme_id=1)
        db.session.add(king)
        db.session.commit()
        return {"king": {str(king.id): king.to_dict()}}, http.CREATED

    except ValidationError as e:
        return {
            "message": "validation error",
            "errors": {
                err["loc"][0]: err["msg"] for err in e.errors()
            },
        }, http.UNPROCESSABLE_ENTITY

    except IntegrityError as e:
        db.session.rollback()
        field = "email" if "email" in str(e.orig) else "nick"

        return {
            "message": "account conflict",
            "errors": {field: f"{field} is taken"},
        }, http.CONFLICT
