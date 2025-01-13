"""endpoints for themes."""

from flask import Blueprint
from flask_login import login_required

theme_blueprint = Blueprint("theme", __name__, url_prefix="theme")


@theme_blueprint.route("/", methods=["POST"])
@login_required
def create():
    """Create a new theme."""
    print("TODO: theme create")
    exit(-1)


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
