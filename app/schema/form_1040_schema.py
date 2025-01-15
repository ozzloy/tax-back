"""Schema for form_1040 model."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)


class FilingStatus(Enum):
    """Filing statuses for form 1040."""

    SINGLE = "Single"
    MARRIED_FILING_JOINTLY = "Married Filing Jointly"
    MARRIED_FILING_SEPARATELY = "Married Filing Separately"
    HEAD_OF_HOUSEHOLD = "Head of Household"
    QUALIFYING_WIDOW = "Qualifying Widow(er)"


filing_statuses = [status.value for status in FilingStatus]


class Form1040InputSchema(BaseModel):
    """Validate form_1040 create/edit requests."""

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[\w\s\-'#,\./]+$",
        description="name for king to remember this form by",
    )
    tax_year: Optional[int] = Field(
        default=None, gt=1912, le=datetime.now().year + 1
    )
    filer_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="id of the human filing this form",
    )
    spouse_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="id of spouse filing this form",
    )
    address_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="id of address of human filing this form",
    )
    wages: Optional[float] = Field(
        default=None,
        description="form w2, box 1",
    )
    withholdings: Optional[float] = Field(
        default=None,
        description="form w2, box 2",
    )
    filing_status: Optional[str] = Field(default=None)

    @field_validator("wages")
    def wages_must_exceed_withholdings(cls, v, values):
        """Wages must be greater than or equal to withholdings."""
        withholdings = values.data.get("withholdings")
        if v is not None and withholdings is not None:
            if v < withholdings:
                raise ValueError(
                    "wages must be greater than or equal to withholdings"
                )
        return v

    @field_validator("withholdings")
    def withholdings_must_not_exceed_wages(cls, v, values):
        """Withholdings must be less than or equal to wages."""
        wages = values.data.get("wages")
        if v is not None and wages is not None:
            if v > wages:
                raise ValueError(
                    "withholdings must be less than or equal to wages"
                )
        return v

    @field_validator("filing_status")
    def validate_filing_status(cls, filing_status: str) -> str:
        """Ensure state code is valid."""
        if filing_status and filing_status not in filing_statuses:
            raise ValueError(
                f"invalid filing status: {filing_status}. "
                f"must be one of: {filing_statuses}"
            )
        return filing_status

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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "My 1040 for 2024",
                "tax_year": 2024,
                "filer_id": 5,
                "spouse_id": 6,
                "address_id": 4,
                "wages": 51_234.2,
                "withholdings": 12_345.67,
                "filing_status": "Single",
            }
        },
        str_strip_whitespace=True,
    )


class Form1040Schema(BaseModel):
    """Validate form_1040 responses."""

    id: int
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r"^[\w\s\-'#,\./]+$",
        description="name for king to remember this form by",
    )
    tax_year: Optional[int] = Field(default=None, gt=0)
    filer_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="id of the human filing this form",
    )
    spouse_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="id of spouse filing this form",
    )
    address_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="id of address of human filing this form",
    )
    wages: Optional[float] = Field(
        default=None,
        gt=0,
        description="form w2, box 1",
    )
    withholdings: Optional[float] = Field(
        default=None,
        gt=0,
        description="form w2, box 2",
    )
    filing_status: Optional[str] = Field(default=None)
    king_id: int = Field(
        gt=0, description="id of king that created this form"
    )
    created: datetime
    updated: datetime

    @field_validator("filing_status")
    def validate_filing_status(cls, filing_status: str) -> str:
        """Ensure state code is valid."""
        valid_statuses = [status.value for status in FilingStatus]
        if filing_status and filing_status not in valid_statuses:
            raise ValueError(
                f"invalid filing status: {filing_status}. "
                f"must be one of: {valid_statuses}"
            )
        return filing_status

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetimes for JSON."""
        return dt.isoformat()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "My 1040 for 2024",
                "tax_year": 2024,
                "filer_id": 5,
                "spouse_id": 6,
                "address_id": 4,
                "wages": 51_234.2,
                "withholdings": 12_345.67,
                "filing_status": "Single",
                "king_id": 7,
            }
        },
        str_strip_whitespace=True,
    )

    @field_validator("wages")
    def wages_must_exceed_withholdings(cls, v, values):
        """Wages must be greater than or equal to withholdings."""
        withholdings = values.get("withholdings")
        if v is not None and withholdings is not None:
            if v < withholdings:
                raise ValueError(
                    "wages must be greater than or equal to withholdings"
                )
        return v

    @field_validator("withholdings")
    def withholdings_must_not_exceed_wages(cls, v, values):
        """Withholdings must be less than or equal to wages."""
        wages = values.get("wages")
        if v is not None and wages is not None:
            if v > wages:
                raise ValueError(
                    "withholdings must be less than or equal to wages"
                )
        return v

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
