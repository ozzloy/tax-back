"""address ORM."""

from datetime import datetime
from typing import Optional

from app.db import db
from app.schema import AddressSchema


class Address(db.Model):
    """address ORM."""

    id: int = db.Column(db.Integer, primary_key=True)
    street: Optional[str] = db.Column(db.String(255), nullable=True)
    city: Optional[str] = db.Column(db.String(255), nullable=True)
    state: Optional[str] = db.Column(db.String(2), nullable=True)
    zip: Optional[str] = db.Column(db.String(10), nullable=True)
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

    king = db.relationship("King", back_populates="addresses")
    form_1040s = db.relationship(
        "Form1040", back_populates="addresses"
    )

    def to_dict(self):
        """Public info about this address."""
        return AddressSchema.model_validate(self).model_dump()
