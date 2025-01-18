"""make initial themes."""

from sqlalchemy import and_

from app.db import db
from app.model import Theme
from app.schema import ThemeCreateSchema

theme_seeds = [
    {
        "name": "night",
        "foreground_color": "chartreuse",
        "background_color": "#111",
        "king_id": None,
    },
    {
        "name": "light",
        "foreground_color": "black",
        "background_color": "whitesmoke",
        "king_id": None,
    },
]


def seed_theme():
    """Insert themes into db."""
    for theme_data in theme_seeds:
        king_id = theme_data["king_id"]
        name = theme_data["name"]
        theme_data = ThemeCreateSchema(**theme_data).model_dump()
        theme_data["king_id"] = king_id
        theme = Theme.query.filter(
            and_(
                Theme.king_id == king_id,
                Theme.name == name,
            )
        ).first()
        if theme:
            for name, value in theme_data.items():
                setattr(theme, name, value)
        else:
            theme = Theme(**theme_data)
            db.session.add(theme)

    db.session.commit()


def undo_theme():
    """Remove themes from db."""
    pass
