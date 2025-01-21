"""make demo king."""

from sqlalchemy import and_, or_
from sqlalchemy.exc import MultipleResultsFound

from app.db import db
from app.model import King
from app.model import Theme
from app.schema import KingSignupSchema
from .theme_seed import theme_seeds

king_seeds = [
    {
        "email": "bob@example.com",
        "nick": "bob",
        "password": "password",
        "theme_id": 0,
    }
]


def seed_king():
    """Insert demo king into db."""
    for king_data in king_seeds:
        email = king_data["email"]
        nick = king_data["nick"]
        password = king_data["password"]

        extant_kings = (
            db.session.query(King)
            .filter(
                or_(
                    King.email == email,
                    King.nick == nick,
                )
            )
            .all()
        )

        king_count = len(extant_kings)
        if 1 < king_count:
            raise MultipleResultsFound(
                "Found multiple kings with email "
                + email
                + " or nick "
                + nick
            )

        system_theme_index = king_data["theme_id"]
        king_data = KingSignupSchema(**king_data).model_dump()

        system_themes = [
            db.session.query(Theme)
            .filter(Theme.king_id.is_(None))
            .order_by(Theme.created)
            .first()
            for theme_seed in theme_seeds
        ]
        system_theme_id = system_themes[system_theme_index].id
        king_data["theme_id"] = system_theme_id

        if 0 == king_count:
            king = King(**king_data)
            db.session.add(king)
        else:
            king = extant_kings[0]
            for key, value in king_data.items():
                setattr(king, key, value)

        db.session.commit()


def undo_king():
    """Remove seed kings from db."""
    # TODO
    # currently unimplemented because the whole db just
    #   gets nuked and resurrected from 0 on every run
    pass
