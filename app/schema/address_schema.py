"""Schema for address model."""

from datetime import datetime
from typing import Optional

import us
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

# Get all state abbreviations
state_abbreviations = [state.abbr for state in us.states.STATES]


class AddressInputSchema(BaseModel):
    """Validate address creation requests."""

    street: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[\w\s\-'#,\./]+$",
    )
    city: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[a-zA-Z\s\-'\.]+$",
    )
    state: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern=r"^[A-Z]{2}$",
    )
    zip: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=10,
        pattern=r"^\d{5}(?:-\d{4})?$",
    )

    @field_validator("state")
    def validate_state(cls, state: str) -> str:
        """Ensure state code is valid."""
        if state and state not in state_abbreviations:
            raise ValueError(f"Invalid state code: {state}")
        return state

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "street": "1600 Pennsylvania Ave.",
                "city": "Beverly Hills",
                "state": "CA",
                "zip": "90210",
            }
        },
        str_strip_whitespace=True,
    )

    @model_validator(mode="before")
    def convert_empty_strings_to_none(cls, values):
        """Convert empty strings to None for optional fields."""
        for field in values:
            if (
                isinstance(values[field], str)
                and not values[field].strip()
            ):
                values[field] = None
        return values


class AddressSchema(BaseModel):
    """Address data returned in responses."""

    id: int
    street: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[ 0-9A-Za-z\s\-'#,\.]+$",
    )
    city: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[ a-zA-Z\-]+$",
    )
    state: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern=r"^[A-Z]{2}$",
    )
    zip: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=10,
        pattern=r"^\d{5}(?:-\d{4})?$",
    )
    king_id: int = Field(gt=0)
    created: datetime
    updated: datetime

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetimes for JSON."""
        return dt.isoformat()

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "street": "1600 Pennsylvania Ave.",
                "city": "Beverly Hills",
                "state": "CA",
                "zip": "90210",
                "king_id": 1,
                "created": "2024-01-13T12:00:00Z",
                "updated": "2024-01-13T12:00:00Z",
            }
        },
        str_strip_whitespace=True,
    )
