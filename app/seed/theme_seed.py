"""make initial themes."""

from sqlalchemy import and_

from app.db import db
from app.model import Theme

theme_seeds = [
    {
        "name": "night",
        "text_color": "chartreuse",
        "background_color": "black",
        "king_id": None,
    },
    {
        "name": "light",
        "text_color": "white",
        "background_color": "black",
        "king_id": None,
    },
]


def seed_theme():
    """Insert themes into db."""
    for theme_data in theme_seeds:
        theme = Theme.query.filter(
            and_(
                Theme.king_id == theme_data["king_id"],
                Theme.name == theme_data["name"],
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
