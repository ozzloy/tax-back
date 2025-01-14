"""generate king related data, like king signup."""

import factory
from faker import Faker

from app.schema import KingSignupSchema

fake = Faker()


class KingStub(factory.Factory):
    """Generate king signup data."""

    class Meta:
        """The meta class for the factory."""

        model = KingSignupSchema

    email = factory.LazyFunction(lambda: fake.email())
    nick = factory.LazyFunction(lambda: fake.user_name())
    password = factory.LazyFunction(lambda: fake.password(length=6))
