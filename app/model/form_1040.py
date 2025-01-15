"""form_1040 ORM."""

from datetime import datetime
from typing import Optional

from app.db import db
from app.schema import Form1040Schema


class Form1040(db.Model):
    """form 1040 ORM."""

    id: int = db.Column(db.Integer, primary_key=True)
    name: Optional[str] = db.Column(db.String(255), nullable=True)
    tax_year: Optional[int] = db.Column(db.Integer, nullable=True)
    filing_status: Optional[str] = db.Column(
        db.String(255), nullable=True
    )
    filer_id: Optional[int] = db.Column(
        db.Integer(), db.ForeignKey("human.id"), nullable=True
    )
    spouse_id: Optional[int] = db.Column(
        db.Integer(), db.ForeignKey("human.id"), nullable=True
    )
    address_id: Optional[int] = db.Column(
        db.Integer(), db.ForeignKey("address.id"), nullable=True
    )
    wages: Optional[float] = db.Column(db.Float(), nullable=True)
    withholdings: Optional[float] = db.Column(
        db.Float(), nullable=True
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

    king = db.relationship("King", back_populates="form_1040s")
    addresses = db.relationship(
        "Address", back_populates="form_1040s"
    )
    filer = db.relationship(
        "Human", back_populates="form_1040s", foreign_keys=[filer_id]
    )
    spouse = db.relationship(
        "Human",
        back_populates="spouse_form_1040s",
        foreign_keys=[spouse_id],
    )

    def to_dict(self):
        """Public info about this form 1040."""
        return Form1040Schema.model_validate(self).model_dump()
