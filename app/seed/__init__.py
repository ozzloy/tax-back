"""all initial values in the system."""

from .theme_seed import seed_theme


def seed():
    """Put data into db."""
    seed_theme()
