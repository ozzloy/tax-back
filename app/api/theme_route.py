"""endpoints for themes."""

from flask import abort, Blueprint, request
from flask_login import current_user as current_king, login_required
from http import HTTPStatus as http

from app import db
from app.model import Theme
from app.schema import StatePartialSchema, ThemeCreateSchema

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
    db.session.commit()

    state_data = {"theme": {str(theme.id): theme.to_dict()}}

    partial_state = StatePartialSchema(**state_data).model_dump(
        exclude_none=True
    )
    return partial_state, http.CREATED


@theme_blueprint.route("/", methods=["GET"])
@login_required
def read_all():
    """Read all themes."""
    themes = db.session.query(Theme).all()

    slice = {
        "theme": {str(theme.id): theme.to_dict() for theme in themes}
    }
    partial_state = StatePartialSchema(**slice).model_dump(
        exclude_none=True
    )
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
def update():
    """Update a theme."""
    print("TODO: theme update")
    exit(-1)


@theme_blueprint.route("/", methods=["DELETE"])
@login_required
def delete():
    """Delete a theme."""
    print("TODO: theme delete")
    exit(-1)
