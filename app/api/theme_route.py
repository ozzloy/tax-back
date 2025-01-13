"""endpoints for themes."""

from flask import Blueprint, request
from flask_login import current_user as current_king, login_required
from http import HTTPStatus as http

from app import db
from app.model import Theme
from app.schema import StateSchema, ThemeCreateSchema

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

    themes = db.session.query(Theme).all()

    state_data = {
        "current_king_id": current_king.id,
        "king": {str(current_king.id): current_king.to_dict()},
        "theme": {str(theme.id): theme.to_dict() for theme in themes},
    }

    state = StateSchema(**state_data).model_dump()
    return state, http.OK


@theme_blueprint.route("/", methods=["POST"])
@login_required
def read_all():
    """Read all themes."""
    print("TODO: theme read all")
    exit(-1)


@theme_blueprint.route("/<int:theme_id>", methods=["GET"])
@login_required
def read():
    """Read a theme."""
    print("TODO: theme read")
    exit(-1)


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
