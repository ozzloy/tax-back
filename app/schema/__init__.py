"""provide schema for all json objects."""

from .king_schema import (
    KingPrivateSchema,
    KingPublicSchema,
    KingSignupSchema,
)
from .state_schema import StateSchema

__all__ = [
    "KingPrivateSchema",
    "KingPublicSchema",
    "KingSignupSchema",
    "StateSchema",
]
