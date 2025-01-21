"""endpoints for kings."""

from http import HTTPStatus as http

from app import db
from app.model import King, Theme
from app.schema import (
    KingSignupSchema,
    KingUpdateSchema,
    StatePartialSchema,
)
from flask import Blueprint, abort, request
from flask_login import current_user as current_king
from flask_login import login_required
from flask_login import logout_user as logout_king

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
    partial_state = StatePartialSchema.model_validate(
        state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.CREATED


@king_blueprint.route("/", methods=["GET"])
@login_required
def read():
    """Look up info on all kings."""
    kings = db.session.query(King).all()

    state_data = {
        "current_king_id": current_king.id,
        "king": {str(current_king.id): king for king in kings},
    }
    state_data["king"][
        str(current_king.id)
    ] = current_king.to_private_dict()

    partial_state = StatePartialSchema(**state_data).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@king_blueprint.route("/", methods=["PUT"])
@login_required
def update():
    """Update current king's account details."""
    update_data = KingUpdateSchema.model_validate(
        request.json
    ).model_dump(exclude_none=True)

    king = db.session.get(King, current_king.id)

    if king.id != current_king.id:
        abort(http.NOT_FOUND)

    # update each provided field
    for field, value in update_data.items():
        setattr(king, field, value)

    db.session.commit()

    # prepare response
    state_data = {
        "current_king_id": current_king.id,
        "king": {str(king.id): king.to_private_dict()},
    }
    partial_state = StatePartialSchema.model_validate(
        state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK


@king_blueprint.route("/", methods=["DELETE"])
@login_required
def delete():
    """Delete the currently logged in king's account."""
    # get current king from database
    king_id = current_king.id
    king = db.session.get(King, king_id)

    # delete the king
    db.session.delete(king)
    db.session.commit()

    logout_king()
    return {
        "current_king_id": None,
        "king": {str(king_id): None},
    }, http.OK
