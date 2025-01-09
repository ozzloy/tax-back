from flask import Blueprint
from app.model import King

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    data = request.json

    if not data or "nick" not in data:
        return {
            "message": "field missing",
            "errors": {"nick": "nick is required"},
        }, 400

    king = User(nick=data["nick"])
    db.session.add(king)

    try:
        db.session.commit()
        return {"king": {str(king.id): king.to_dict()}}
    except Exception as e:
        db.session.rollback()
        return {
            "message": "internal server error",
            "errors": {"exception": str(e)},
        }, 500


@king_blueprint.route("/")
def read_all():
    kings = King.query.all()
    return {"king": {str(king.id): king.to_dict() for king in kings}}
