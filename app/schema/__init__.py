"""provide schema for all json objects."""

from .king_schema import (
    KingPrivateSchema,
    KingPublicSchema,
    KingSignupSchema,
    KingUpdateSchema,
)
from .session_schema import SessionLoginSchema
from .state_schema import StateSchema
from .theme_schema import (
    ThemeCreateSchema,
    ThemeUpdateSchema,
    ThemeResponseSchema,
)

__all__ = [
    "KingPrivateSchema",
    "KingPublicSchema",
    "KingSignupSchema",
    "KingUpdateSchema",
    "SessionLoginSchema",
    "StateSchema",
    "ThemeCreateSchema",
    "ThemeUpdateSchema",
    "ThemeResponseSchema",
]
