from app import db
from datetime import datetime


class King(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(70), unique=True, nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nick": self.nick,
            "created": self.created.isoformat(),
            "updated": self.created.isoformat(),
        }
