"""provide schema for all json objects."""

from .human_schema import (
    HumanCreateSchema,
    HumanUpdateSchema,
    HumanSchema,
)
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
    ThemeSchema,
    valid_colors,
)

__all__ = [
    "HumanCreateSchema",
    "HumanUpdateSchema",
    "HumanSchema",
    "KingPrivateSchema",
    "KingPublicSchema",
    "KingSignupSchema",
    "KingUpdateSchema",
    "SessionLoginSchema",
    "StateSchema",
    "StatePartialSchema",
    "ThemeCreateSchema",
    "ThemeUpdateSchema",
    "ThemeSchema",
    "valid_colors",
]
