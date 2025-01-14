"""generate humans."""

import string

import factory
from faker import Faker

from app.schema import HumanCreateSchema

fake = Faker()


class HumanStub(factory.Factory):
    """Generate human creation data."""

    class Meta:
        """The meta class for human factory."""

        model = HumanCreateSchema

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    middle_initial = factory.LazyAttribute(
        lambda _: fake.random_element(string.ascii_uppercase)
    )
    last_name = factory.LazyAttribute(lambda _: fake.last_name())


class DifferentHumanStub(HumanStub):
    """generate different human data from an original human."""

    @classmethod
    def create_different(cls, original_data):
        """Create human ensuring all fields have new values."""
        # get unique values excluding the originals
        unique_fake = Faker()
        unique_fake.unique.exclude_first_names = {
            original_data["first_name"]
        }

        different_first = unique_fake.unique.first_name()

        # for middle initial, remove the original from possible choices
        available_initials = set(string.ascii_uppercase) - {
            original_data["middle_initial"]
        }
        different_middle = fake.random_element(
            list(available_initials)
        )

        # get unique last name
        unique_fake.unique.exclude_last_names = {
            original_data["last_name"]
        }
        different_last = unique_fake.unique.last_name()

        return HumanCreateSchema(
            first_name=different_first,
            middle_initial=different_middle,
            last_name=different_last,
        )
