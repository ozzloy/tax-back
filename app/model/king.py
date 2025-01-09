from flask_login import UserMixin as KingMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app import db
from datetime import datetime


class King(db.Model, KingMixin):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(70), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    theme_id = db.Column(db.Integer, nullable=True)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nick": self.nick,
            "email": self.email,
            "created": self.created.isoformat(),
            "updated": self.created.isoformat(),
        }
