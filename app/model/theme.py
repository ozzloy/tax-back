"""theme ORM."""

from datetime import datetime

from app.db import db
from app.schema import ThemeDictSchema


class Theme(db.Model):
    """theme ORM."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    text_color = db.Column(db.String(255), nullable=False)
    background_color = db.Column(db.String(255), nullable=False)
    king_id = db.Column(
        db.Integer, db.ForeignKey("king.id"), nullable=True
    )
    created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    king = db.relationship("King", back_populates="themes")

    __table_args__ = (
        db.UniqueConstraint(
            "king_id", "name", name="unique_king_theme"
        ),
    )

    def to_dict(self):
        """Public info about this theme."""
        return ThemeDictSchema.model_validate(self).model_dump()
