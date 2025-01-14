"""generate all the data for tests."""

from .human_stub import DifferentHumanStub, HumanStub
from .king_stub import KingStub
from .session_stub import SessionLoginStub
from .theme_stub import ThemeStub

__all__ = [
    "DifferentHumanStub",
    "HumanStub",
    "KingStub",
    "SessionLoginStub",
    "ThemeStub",
]
