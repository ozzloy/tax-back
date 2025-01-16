"""generate themes."""

import random
import string

import factory
from app.schema import ThemeCreateSchema, web_colors
from faker import Faker

fake = Faker()


def get_hex_color():
    """Generate random hex color string."""
    hex_chars = string.hexdigits[:16].lower()
    k = 3 if random.choice([True, False]) else 6
    return "#" + "".join(random.choices(hex_chars, k=k))


def get_random_color():
    return random.choice(
        [
            fake.word(ext_word_list=web_colors),
            get_hex_color(),
        ]
    )


class ThemeStub(factory.Factory):
    """Generate theme creation data."""

    class Meta:
        """The meta class for theme factory."""

        model = ThemeCreateSchema

    _counter = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(
        lambda obj: f"{fake.bs()} {obj._counter}"
    )
    text_color = factory.LazyFunction(get_random_color)
    background_color = factory.LazyFunction(get_random_color)
