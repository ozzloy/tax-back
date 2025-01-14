"""king ORM."""

from datetime import datetime
from flask_login import UserMixin as KingMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.db import db
from app.schema import KingPublicSchema


class King(db.Model, KingMixin):
    """king ORM."""

    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    theme_id = db.Column(db.Integer, nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    themes = db.relationship("Theme", back_populates="king")
    humans = db.relationship("Human", back_populates="king")
    addresses = db.relationship("Address", back_populates="king")

    @property
    def password(self):
        """Use the password_hash rather than the password."""
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches stored hash."""
        return check_password_hash(self.password, password)

    def to_private_dict(self):
        """Private data about this king."""
        return {
            "id": self.id,
            "nick": self.nick,
            "email": self.email,
            "theme_id": self.theme_id,
            "created": self.created.isoformat(),
            "updated": self.created.isoformat(),
        }

    def to_dict(self):
        """Public data about this king."""
        return KingPublicSchema.model_validate(self).model_dump()
