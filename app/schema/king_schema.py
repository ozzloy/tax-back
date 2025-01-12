"""schema for king model."""

from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_serializer,
)


class KingSignupSchema(BaseModel):
    """validate signup requests."""

    email: EmailStr
    nick: str = Field(min_length=1)
    password: str = Field(min_length=6)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "bob@example.com",
                "nick": "bob",
                "password": "secret password",
            }
        }
    )


class KingPrivateSchema(BaseModel):
    """data that a king sees about itself."""

    id: int
    email: str
    nick: str
    theme_id: int
    created: datetime
    updated: datetime


class KingPublicSchema(BaseModel):
    """data that every king sees about other kings."""

    id: int
    nick: str
    created: datetime
    updated: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime):
        """Serialize datetimes for JSON."""
        return dt.isoformat()
