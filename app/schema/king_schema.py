"""schema for king model"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class KingCreate(BaseModel):
    email: EmailStr = Field(
        ..., description="Email address of the king"
    )
    nick: str = Field(
        ..., min_length=1, description="Nickname of the king"
    )
    password: str = Field(
        ..., min_length=1, description="Password for the account"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "bob@example.com",
                "nick": "bob",
                "password": "secret password",
            }
        }
    )


class KingResponse(BaseModel):
    id: int
    email: str
    nick: str
    theme_id: int

    model_config = ConfigDict(from_attributes=True)
