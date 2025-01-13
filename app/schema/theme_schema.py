"""Schema for theme model."""

from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)
from typing import Optional
from webcolors import names as get_webcolor_names


valid_colors = get_webcolor_names()


class ThemeCreateSchema(BaseModel):
    """Validate theme creation requests."""

    name: str = Field(min_length=1)
    text_color: str = Field(min_length=1)
    background_color: str = Field(min_length=1)

    @field_validator("text_color", "background_color")
    @classmethod
    def calidate_color(cls, value: str) -> str:
        """Ensure that color comes from web color names."""
        color = value.lower()
        if color not in valid_colors:
            raise ValueError("color must be html colorname")
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
    def calidate_color(cls, value: str) -> str:
        """Ensure that color comes from web color names."""
        color = value.lower()
        if color not in valid_colors:
            raise ValueError("color must be html colorname")
        return color


class ThemeResponseSchema(BaseModel):
    """Theme data returned in responses."""

    id: int
    name: str
    text_color: str
    background_color: str
    created: datetime
    updated: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("text_color", "background_color")
    @classmethod
    def calidate_color(cls, value: str) -> str:
        """Ensure that color comes from web color names."""
        color = value.lower()
        if color not in valid_colors:
            raise ValueError("color must be html colorname")
        return color

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime):
        """Serialize datetimes for JSON."""
        return dt.isoformat()
