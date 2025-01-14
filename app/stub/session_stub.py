"""generate session login, logout data."""

import factory
from faker import Faker

from app.schema import SessionLoginSchema

fake = Faker()


class SessionLoginStub(factory.Factory):
    """Generate session login data."""

    class Meta:
        """The meta class for the factory."""

        model = SessionLoginSchema

    email = factory.LazyFunction(lambda: fake.email())
    password = factory.LazyFunction(lambda: fake.password(length=6))
