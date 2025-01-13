"""validate state and its slices."""

from pydantic import BaseModel, field_validator
from typing import Dict, Optional, Union


from .king_schema import (
    KingPrivateSchema,
    KingPublicSchema,
)
from .theme_schema import ThemeDictSchema


class StateSchema(BaseModel):
    """schema for application state."""

    current_king_id: Optional[int]
    king: Dict[str, Union[KingPublicSchema, KingPrivateSchema]]
    theme: Dict[str, ThemeDictSchema]

    @field_validator("king", "theme")
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
    theme: Optional[Dict[str, ThemeDictSchema]] = None

    @field_validator("king", "theme")
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
