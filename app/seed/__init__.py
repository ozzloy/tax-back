"""all initial values in the system."""

from .theme_seed import seed_theme
from .king_seed import seed_king


def seed():
    """Put data into db."""
    seed_theme()
    seed_king()
