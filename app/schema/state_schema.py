"""validate state and its slices."""

from pydantic import BaseModel, field_validator
from typing import Dict, Optional, Union


from .king_schema import (
    KingPrivateSchema,
    KingPublicSchema,
)


class StateSchema(BaseModel):
    """schema for application state."""

    current_king_id: Optional[int]
    king: Dict[str, Union[KingPublicSchema, KingPrivateSchema]]

    @field_validator("king")
    @classmethod
    def validate_king_ids(cls, king_slice):
        """Make sure slice id for king matches inner king's id."""
        if king_slice:
            for king_id_str, king in king_slice.items():
                if str(king.id) != king_id_str:
                    raise ValueError(
                        "King ID mismatch: slice key"
                        + king_id_str
                        + "does not match king.id "
                        + str(king.id)
                    )
        return king_slice
