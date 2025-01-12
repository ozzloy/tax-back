"""verify session (login, logout) data structures."""

from pydantic import ConfigDict, EmailStr, Field


from .base import DictModel


class SessionLoginSchema(DictModel):
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
