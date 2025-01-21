"""endpoints for humans."""

from flask import abort, Blueprint, request
from flask_login import current_user as current_king, login_required
from http import HTTPStatus as http
from sqlalchemy.exc import IntegrityError

from app import db
from app.model import Human
from app.schema import (
    StatePartialSchema,
    HumanCreateSchema,
    HumanUpdateSchema,
)

human_blueprint = Blueprint("human", __name__, url_prefix="human")


@human_blueprint.route("/", methods=["POST"])
@login_required
def create():
    """Create a new human."""
    human_data = HumanCreateSchema.model_validate(
        request.json
    ).model_dump()
    human_data["king_id"] = current_king.id

    human = Human(**human_data)

    db.session.add(human)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to create human"},
        }, http.CONFLICT

    state_data = {"human": {str(human.id): human.to_dict()}}

    partial_state = StatePartialSchema(**state_data).model_dump(
        exclude_none=True
    )
    return partial_state, http.CREATED


@human_blueprint.route("/", methods=["GET"])
@login_required
def read_all():
    """Read all humans."""
    humans = (
        db.session.query(Human)
        .filter(Human.king_id == current_king.id)
        .all()
    )

    slice = {
        "human": {str(human.id): human.to_dict() for human in humans}
    }
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@human_blueprint.route("/<int:human_id>", methods=["GET"])
@login_required
def read(human_id):
    """Read a human."""
    # get human with matching id
    human = db.session.get(Human, human_id) or abort(http.NOT_FOUND)
    slice = {"human": {str(human.id): human.to_dict()}}
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@human_blueprint.route("/<int:human_id>", methods=["PUT"])
@login_required
def update(human_id):
    """Update a human."""
    update_data = HumanUpdateSchema.model_validate(
        request.json
    ).model_dump(exclude_none=True)

    human = db.session.get(Human, human_id) or abort(http.NOT_FOUND)

    if human.king_id != current_king.id:
        abort(http.NOT_FOUND)

    for field, value in update_data.items():
        setattr(human, field, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to update human"},
        }, http.CONFLICT

    partial_state_data = {"human": {str(human.id): human.to_dict()}}
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK


@human_blueprint.route("/<int:human_id>", methods=["DELETE"])
@login_required
def delete(human_id):
    """Delete a human."""
    human = db.session.get(Human, human_id) or abort(http.NOT_FOUND)
    human_id = human.id

    db.session.delete(human)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to delete human"},
        }, http.CONFLICT

    partial_state_data = {"human": {str(human_id): None}}
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK
