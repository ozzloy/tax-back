"""endpoints for addresss."""

from http import HTTPStatus as http
from sqlalchemy.exc import IntegrityError

from app import db
from app.model import Address
from app.schema import AddressInputSchema, StatePartialSchema
from flask import Blueprint, abort, request
from flask_login import current_user as current_king
from flask_login import login_required

address_blueprint = Blueprint(
    "address", __name__, url_prefix="address"
)


@address_blueprint.route("/", methods=["POST"])
@login_required
def create():
    """Create a new address."""
    address_data = AddressInputSchema.model_validate(
        request.json
    ).model_dump()
    address_data["king_id"] = current_king.id

    address = Address(**address_data)

    db.session.add(address)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to create address"},
        }, http.CONFLICT

    state_data = {"address": {str(address.id): address.to_dict()}}

    partial_state = StatePartialSchema(**state_data).model_dump(
        exclude_none=True
    )
    return partial_state, http.CREATED


@address_blueprint.route("/", methods=["GET"])
@login_required
def read_all():
    """Read all addresss."""
    addresss = db.session.query(Address).all()

    slice = {
        "address": {
            str(address.id): address.to_dict() for address in addresss
        }
    }
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@address_blueprint.route("/<int:address_id>", methods=["GET"])
@login_required
def read(address_id):
    """Read a address."""
    # get address with matching id
    address = db.session.get(Address, address_id) or abort(
        http.NOT_FOUND
    )
    slice = {"address": {str(address.id): address.to_dict()}}
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@address_blueprint.route("/<int:address_id>", methods=["PUT"])
@login_required
def update(address_id):
    """Update a address."""
    update_data = AddressInputSchema.model_validate(
        request.json
    ).model_dump(exclude_none=True)

    address = db.session.get(Address, address_id) or abort(
        http.NOT_FOUND
    )

    if address.king_id != current_king.id:
        abort(http.NOT_FOUND)

    for field, value in update_data.items():
        setattr(address, field, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to update address"},
        }, http.CONFLICT

    partial_state_data = {
        "address": {str(address.id): address.to_dict()}
    }
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK


@address_blueprint.route("/<int:address_id>", methods=["DELETE"])
@login_required
def delete(address_id):
    """Delete a address."""
    address = db.session.get(Address, address_id) or abort(
        http.NOT_FOUND
    )
    address_id = address.id

    db.session.delete(address)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        errors = {}
        return {
            "message": "integrity error",
            "errors": {"_error": "unable to delete address"},
        }, http.CONFLICT

    partial_state_data = {"address": {str(address_id): None}}
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK
