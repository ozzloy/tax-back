"""Schema for theme model."""

import re
from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)
from webcolors import names as get_webcolor_names

web_colors = get_webcolor_names()


def is_hex_color(color):
    hex_regex = r"^#[\da-f]{3}(?:[\da-f]{3})?$"
    return bool(re.match(hex_regex, color))


def is_web_color(color):
    return color in web_colors


class ThemeCreateSchema(BaseModel):
    """Validate theme creation requests."""

    name: str = Field(min_length=1)
    text_color: str = Field(min_length=1)
    background_color: str = Field(min_length=1)

    @field_validator("text_color", "background_color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        """Ensure that color comes from web color names."""
        color = value.lower()
        if not (is_web_color(color) or is_hex_color(color)):
            message = "color must be html colorname or hex code"
            raise ValueError(message)
        return color

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "blue steele",
                "text_color": "blue",
                "background_color": "steelblue",
            }
        }
    )


class ThemeUpdateSchema(BaseModel):
    """Validate theme update requests."""

    name: Optional[str] = Field(default=None, min_length=1)
    text_color: Optional[str] = Field(default=None, min_length=1)
    background_color: Optional[str] = Field(
        default=None, min_length=1
    )

    @field_validator("text_color", "background_color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        """Ensure that color comes from web color names."""
        color = value.lower()
        if not (is_web_color(color) or is_hex_color(color)):
            message = "color must be html colorname or hex code"
            raise ValueError(message)
        return color


class ThemeSchema(BaseModel):
    """Theme data returned in responses."""

    id: int
    name: str = Field(min_length=1)
    text_color: str
    background_color: str
    king_id: Optional[int] = None
    created: datetime
    updated: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("text_color", "background_color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        """Ensure that color comes from web color names."""
        color = value.lower()
        if not (is_web_color(color) or is_hex_color(color)):
            message = "color must be html colorname or hex code"
            raise ValueError(message)
        return color

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime):
        """Serialize datetimes for JSON."""
        return dt.isoformat()
