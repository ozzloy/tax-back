"""human ORM."""

from datetime import datetime
from typing import Optional

from app.db import db
from app.schema import HumanSchema


class Human(db.Model):
    """human ORM."""

    id: int = db.Column(db.Integer, primary_key=True)
    first_name: Optional[str] = db.Column(
        db.String(255), nullable=True
    )
    middle_initial: Optional[str] = db.Column(
        db.String(1), nullable=True
    )
    last_name: Optional[str] = db.Column(
        db.String(255), nullable=True
    )
    king_id: int = db.Column(
        db.Integer, db.ForeignKey("king.id"), nullable=False
    )
    created: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    king = db.relationship("King", back_populates="humans")

    def to_dict(self):
        """Public info about this human."""
        return HumanSchema.model_validate(self).model_dump()
