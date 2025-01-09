from flask import Blueprint, request

from app import db
from app.model import King
from app.validator import king_validator

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")

    data = request.json

    error_return = king_validator.validate_king_create_data(data)
    if error_return:
        return error_return

    king = King(**data)

    db.session.add(king)

    db.session.commit()

    return {"king": {str(king.id): king.to_dict()}}, 201


@king_blueprint.route("/")
def read_all():
    kings = King.query.all()
    return {"king": {str(king.id): king.to_dict() for king in kings}}
