"""generate all the data for tests."""

from .address_stub import AddressModifiedStub, AddressStub
from .human_stub import DifferentHumanStub, HumanStub
from .king_stub import KingStub
from .session_stub import SessionLoginStub
from .theme_stub import ThemeStub

__all__ = [
    "AddressModifiedStub",
    "AddressStub",
    "DifferentHumanStub",
    "HumanStub",
    "KingStub",
    "SessionLoginStub",
    "ThemeStub",
]
