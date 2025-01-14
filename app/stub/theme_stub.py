"""generate themes."""

import factory
from faker import Faker

from app.schema import ThemeCreateSchema, valid_colors

fake = Faker()


class ThemeStub(factory.Factory):
    """Generate theme creation data."""

    class Meta:
        """The meta class for theme factory."""

        model = ThemeCreateSchema

    _counter = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(
        lambda obj: f"{fake.bs()} {obj._counter}"
    )
    text_color = factory.LazyFunction(
        lambda: fake.word(ext_word_list=valid_colors)
    )
    background_color = factory.LazyFunction(
        lambda: fake.word(ext_word_list=valid_colors)
    )
