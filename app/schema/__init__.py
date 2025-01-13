"""provide schema for all json objects."""

from .king_schema import (
    KingPrivateSchema,
    KingPublicSchema,
    KingSignupSchema,
    KingUpdateSchema,
)
from .session_schema import SessionLoginSchema
from .state_schema import StatePartialSchema, StateSchema
from .theme_schema import (
    ThemeCreateSchema,
    ThemeUpdateSchema,
    ThemeDictSchema,
)

__all__ = [
    "KingPrivateSchema",
    "KingPublicSchema",
    "KingSignupSchema",
    "KingUpdateSchema",
    "SessionLoginSchema",
    "StateSchema",
    "StatePartialSchema",
    "ThemeCreateSchema",
    "ThemeUpdateSchema",
    "ThemeDictSchema",
]
