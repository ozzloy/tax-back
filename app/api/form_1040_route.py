"""endpoints for form_1040s."""

from http import HTTPStatus as http
from sqlalchemy.exc import IntegrityError

from app import db
from app.model import Form1040
from app.schema import Form1040InputSchema, StatePartialSchema
from flask import Blueprint, abort, request
from flask_login import current_user as current_king
from flask_login import login_required

form_1040_blueprint = Blueprint(
    "form_1040", __name__, url_prefix="form_1040"
)


@form_1040_blueprint.route("/", methods=["POST"])
@login_required
def create():
    """Create a new form_1040."""
    form_1040_data = Form1040InputSchema.model_validate(
        request.json
    ).model_dump()
    form_1040_data["king_id"] = current_king.id

    form_1040 = Form1040(**form_1040_data)

    db.session.add(form_1040)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        if "spouse_id" in str(e.orig):
            errors["spouse_id"] = "spouse id not in human table"
        if "filer_id" in str(e.orig):
            errors["filer_id"] = "filer id not in human table"
        if "address_id" in str(e.orig):
            errors["address_id"] = "address id not in address table"
        return {
            "message": "integrity error",
            "errors": errors,
        }, http.CONFLICT

    state_data = {
        "form_1040": {str(form_1040.id): form_1040.to_dict()}
    }

    partial_state = StatePartialSchema(**state_data).model_dump(
        exclude_none=True
    )
    return partial_state, http.CREATED


@form_1040_blueprint.route("/", methods=["GET"])
@login_required
def read_all():
    """Read all form_1040s."""
    form_1040s = (
        db.session.query(Form1040)
        .filter(Form1040.king_id == current_king.id)
        .all()
    )

    slice = {
        "form_1040": {
            str(form_1040.id): form_1040.to_dict()
            for form_1040 in form_1040s
        }
    }
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@form_1040_blueprint.route("/<int:form_1040_id>", methods=["GET"])
@login_required
def read(form_1040_id):
    """Read a form_1040."""
    # get form_1040 with matching id
    form_1040 = db.session.get(Form1040, form_1040_id) or abort(
        http.NOT_FOUND
    )
    slice = {"form_1040": {str(form_1040.id): form_1040.to_dict()}}
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@form_1040_blueprint.route("/<int:form_1040_id>", methods=["PUT"])
@login_required
def update(form_1040_id):
    """Update a form_1040."""
    update_data = Form1040InputSchema.model_validate(
        request.json
    ).model_dump()

    form_1040 = db.session.get(Form1040, form_1040_id) or abort(
        http.NOT_FOUND
    )

    if form_1040.king_id != current_king.id:
        abort(http.NOT_FOUND)

    for field, value in update_data.items():
        setattr(form_1040, field, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        if "spouse_id" in str(e.orig):
            errors["spouse_id"] = "spouse id not in human table"
        if "filer_id" in str(e.orig):
            errors["filer_id"] = "filer id not in human table"
        if "address_id" in str(e.orig):
            errors["address_id"] = "address id not in address table"
        return {
            "message": "integrity error",
            "errors": errors,
        }, http.CONFLICT

    partial_state_data = {
        "form_1040": {str(form_1040.id): form_1040.to_dict()}
    }
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK


@form_1040_blueprint.route("/<int:form_1040_id>", methods=["DELETE"])
@login_required
def delete(form_1040_id):
    """Delete a form_1040."""
    form_1040 = db.session.get(Form1040, form_1040_id) or abort(
        http.NOT_FOUND
    )
    form_1040_id = form_1040.id

    db.session.delete(form_1040)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to delete"},
        }, http.CONFLICT

    partial_state_data = {"form_1040": {str(form_1040_id): None}}
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK
