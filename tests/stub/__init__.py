"""generate all the data for tests."""

from .king_stub import KingSignupStub, KingUpdateStub
from .session_stub import SessionLoginStub
from .theme_stub import ThemeCreateStub

__all__ = [
    "KingSignupStub",
    "KingUpdateStub",
    "SessionLoginStub",
    "ThemeCreateStub",
]
