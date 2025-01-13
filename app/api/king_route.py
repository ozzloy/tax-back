"""endpoints for kings."""

from flask import Blueprint, request
from flask_login import (
    current_user as current_king,
    logout_user as logout_king,
    login_required,
)
from http import HTTPStatus as http

from app import db
from app.model import King, Theme
from app.schema import KingSignupSchema, KingUpdateSchema, StateSchema

king_blueprint = Blueprint("king", __name__, url_prefix="/king")


@king_blueprint.route("/", methods=["POST"])
def create():
    """Create a new king, aka create new account, aka signup."""
    king = KingSignupSchema.model_validate(request.json).model_dump()
    # get all themes where king_id is null. these are system themes
    earliest_system_theme = (
        db.session.query(Theme)
        .filter(Theme.king_id.is_(None))
        .order_by(Theme.created)
        .first()
    )
    king["theme_id"] = earliest_system_theme.id

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


@king_blueprint.route("/", methods=["PUT"])
@login_required
def update():
    """Update current king's account details."""
    update_data = KingUpdateSchema.model_validate(
        request.json
    ).model_dump(exclude_none=True)

    # Get current king from database
    king = db.session.get(King, current_king.id)

    # Update each provided field
    for field, value in update_data.items():
        setattr(king, field, value)

    db.session.commit()

    # Prepare response
    state_data = {
        "current_king_id": current_king.id,
        "king": {str(king.id): king.to_private_dict()},
    }
    state = StateSchema.model_validate(state_data).model_dump()

    return state, http.OK


@king_blueprint.route("/", methods=["DELETE"])
@login_required
def delete():
    """Delete the currently logged in king's account."""
    # get current king from database
    king = db.session.get(King, current_king.id)

    # delete the king
    db.session.delete(king)
    db.session.commit()

    logout_king()
    return {"current_king_id": None}, http.OK
