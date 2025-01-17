"""validate state and its slices."""

from typing import Dict, Optional, Union

from pydantic import BaseModel, field_validator

from .address_schema import AddressSchema
from .form_1040_schema import Form1040Schema
from .human_schema import HumanSchema
from .king_schema import KingPrivateSchema, KingPublicSchema
from .theme_schema import ThemeSchema


class StateSchema(BaseModel):
    """schema for application state."""

    current_king_id: Optional[int]
    king: Dict[str, Union[KingPublicSchema, KingPrivateSchema]]
    theme: Dict[str, ThemeSchema]
    human: Dict[str, HumanSchema]
    address: Dict[str, AddressSchema]
    form_1040: Dict[str, Form1040Schema] = None

    @field_validator("king", "theme", "human", "address", "form_1040")
    @classmethod
    def validate_king_ids(cls, state_slice):
        """Make sure slice id for item matches inner item's id."""
        if state_slice:
            for item_id_str, item in state_slice.items():
                if str(item.id) != item_id_str:
                    raise ValueError(
                        "slice ID mismatch: slice key"
                        + item_id_str
                        + "does not match item.id "
                        + str(item.id)
                    )
        return state_slice


class StatePartialSchema(BaseModel):
    """schema for application state."""

    current_king_id: Optional[int] = None
    king: Optional[
        Dict[str, Union[KingPublicSchema, KingPrivateSchema]]
    ] = None
    theme: Optional[Dict[str, Optional[ThemeSchema]]] = None
    human: Optional[Dict[str, Optional[HumanSchema]]] = None
    address: Optional[Dict[str, Optional[AddressSchema]]] = None
    form_1040: Optional[Dict[str, Optional[Form1040Schema]]] = None

    @field_validator("king", "theme", "human", "address", "form_1040")
    @classmethod
    def validate_king_ids(cls, state_slice):
        """Make sure slice id for item matches inner item's id."""
        if state_slice:
            for item_id_str, item in state_slice.items():
                if item and str(item.id) != item_id_str:
                    raise ValueError(
                        "slice ID mismatch: slice key"
                        + item_id_str
                        + "does not match item.id "
                        + str(item.id)
                    )
        return state_slice
