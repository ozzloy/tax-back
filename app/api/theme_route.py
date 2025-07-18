"""endpoints for themes."""

from flask import abort, Blueprint, request
from flask_login import current_user as current_king, login_required
from http import HTTPStatus as http
from sqlalchemy.exc import IntegrityError

from app import db
from app.model import Theme
from app.schema import (
    StatePartialSchema,
    ThemeCreateSchema,
    ThemeUpdateSchema,
)

theme_blueprint = Blueprint("theme", __name__, url_prefix="theme")


@theme_blueprint.route("/", methods=["POST"])
@login_required
def create():
    """Create a new theme."""
    theme_data = ThemeCreateSchema.model_validate(
        request.json
    ).model_dump()
    theme_data["king_id"] = current_king.id

    theme = Theme(**theme_data)

    db.session.add(theme)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return {
            "message": "theme conflict",
            "errors": {"name": "name is taken"},
        }, http.CONFLICT

    state_data = {"theme": {str(theme.id): theme.to_dict()}}

    partial_state = StatePartialSchema(**state_data).model_dump(
        exclude_none=True
    )
    return partial_state, http.CREATED


@theme_blueprint.route("/", methods=["GET"])
def read_all():
    """Read all themes."""
    if current_king.is_authenticated:
        themes = db.session.query(Theme).all()
    else:
        themes = (
            db.session.query(Theme)
            .filter(Theme.king_id.is_(None))
            .all()
        )

    slice = {
        "theme": {str(theme.id): theme.to_dict() for theme in themes}
    }
    partial_state = StatePartialSchema(**slice).model_dump()
    return partial_state, http.OK


@theme_blueprint.route("/<int:theme_id>", methods=["GET"])
@login_required
def read(theme_id):
    """Read a theme."""
    # get theme with matching id
    theme = db.session.get(Theme, theme_id) or abort(http.NOT_FOUND)
    slice = {"theme": {str(theme.id): theme.to_dict()}}
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
    return partial_state, http.OK


@theme_blueprint.route("/<int:theme_id>", methods=["PUT"])
@login_required
def update(theme_id):
    """Update a theme."""
    update_data = ThemeUpdateSchema.model_validate(
        request.json
    ).model_dump(exclude_none=True)

    theme = db.session.get(Theme, theme_id) or abort(http.NOT_FOUND)

    if theme.king_id != current_king.id:
        abort(http.NOT_FOUND)

    for field, value in update_data.items():
        setattr(theme, field, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return {
            "message": "theme conflict",
            "errors": {"name": "name is taken"},
        }, http.CONFLICT

    partial_state_data = {"theme": {str(theme.id): theme.to_dict()}}
    partial_state = StatePartialSchema.model_validate(
        partial_state_data
    ).model_dump(exclude_none=True)

    return partial_state, http.OK


@theme_blueprint.route("/<int:theme_id>", methods=["DELETE"])
@login_required
def delete(theme_id):
    """Delete a theme."""
    theme = db.session.get(Theme, theme_id) or abort(http.NOT_FOUND)
    theme_id = theme.id

    db.session.delete(theme)
    db.session.commit()

    partial_state = {"theme": {str(theme_id): None}}

    return partial_state, http.OK
