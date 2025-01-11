"""verify session (login, logout) data structures."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SessionLoginSchema(BaseModel):
    """schema for login data.

    example login data structure

    {
        "email": "bob@example.com",
        "password": "secret password"
    }
    """

    email: EmailStr
    password: str = Field(min_length=6)

    model_config = ConfigDict(from_attributes=True)
