"""Schema for human model."""

from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
)
from typing import Optional


class HumanCreateSchema(BaseModel):
    """Validate human creation requests."""

    first_name: str = Field(
        min_length=1, max_length=255, pattern=r"^[A-Za-z\-\s']+$"
    )
    middle_initial: Optional[str] = Field(
        default=None, min_length=1, max_length=1, pattern="^[A-Z]$"
    )
    last_name: str = Field(
        min_length=1, max_length=255, pattern=r"^[A-Za-z\-\s']+$"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Max",
                "middle_initial": "X",
                "last_name": "Power",
            }
        }
    )


class HumanUpdateSchema(BaseModel):
    """Validate human update requests."""

    first_name: Optional[str] = Field(
        min_length=1, max_length=255, pattern=r"^[A-Za-z\-\s']+$"
    )
    middle_initial: Optional[str] = Field(
        min_length=1, max_length=1, pattern="^[A-Z]$"
    )
    last_name: Optional[str] = Field(
        min_length=1, max_length=255, pattern=r"^[A-Za-z\-\s']+$"
    )


class HumanSchema(BaseModel):
    """Human data returned in responses."""

    id: int
    first_name: str = Field(
        min_length=1, max_length=255, pattern=r"^[A-Za-z\-\s']+$"
    )
    middle_initial: str = Field(
        min_length=1, max_length=1, pattern="^[A-Z]$"
    )
    last_name: str = Field(
        min_length=1, max_length=255, pattern=r"^[A-Za-z\-\s']+$"
    )
    king_id: int = Field(gt=0)
    created: datetime
    updated: datetime

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime):
        """Serialize datetimes for JSON."""
        return dt.isoformat()

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "first_name": "Max",
                "middle_initial": "X",
                "last_name": "Power",
                "king_id": 1,
                "created": "2024-01-13T12:00:00",
                "updated": "2024-01-13T12:00:00",
            }
        },
    )
