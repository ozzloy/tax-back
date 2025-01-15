"""generate addresss."""

import random

import factory
from app.schema import AddressInputSchema
from app.schema.address_schema import state_abbreviations
from faker import Faker

fake = Faker()


class AddressStub(factory.Factory):
    """Generate address creation data."""

    class Meta:
        """The meta class for address factory."""

        model = AddressInputSchema

    street = factory.LazyAttribute(lambda _: fake.street_address())
    city = factory.LazyAttribute(lambda _: fake.city())
    state = factory.LazyAttribute(
        lambda _: random.choice(state_abbreviations)
    )

    zip = factory.LazyAttribute(
        lambda _: random.choice(
            [fake.zipcode(), fake.zipcode_plus4()]
        )
    )


class AddressModifiedStub(AddressStub):
    """Generate different address data from an original address."""

    @classmethod
    def create_different(cls, original_data):
        """Create address ensuring all fields have new values."""
        unique_fake = Faker()

        unique_fake.unique.exclude_street_addresses = {
            original_data.street
        }
        different_street = unique_fake.unique.street_address()

        unique_fake.unique.exclude_cities = {original_data.city}
        different_city = unique_fake.unique.city()

        different_state = random.choice(state_abbreviations)
        while different_state == original_data.state:
            different_state = random.choice(state_abbreviations)

        unique_fake.unique.exclude_zipcodes = {original_data.zip}
        unique_fake.unique.exclude_zipcodes_plus4 = {
            original_data.zip
        }
        different_zip = random.choice(
            [
                unique_fake.unique.zipcode_plus4(),
                unique_fake.unique.zipcode(),
            ]
        )

        return AddressInputSchema(
            street=different_street,
            city=different_city,
            state=different_state,
            zip=different_zip,
        )


# Test script
if __name__ == "__main__":
    """
    run from tax directory like this:
    $ PYTHONPATH="." pipenv run python app/stub/address_stub.py
    """
    from pprint import pprint

    # Generate a random address using AddressStub
    print("--- Generated Random Address ---")
    random_address = AddressStub()
    pprint(random_address.__dict__)

    # Generate multiple addresses
    print("\n--- Multiple Random Addresses ---")
    addresses = [AddressStub() for _ in range(3)]
    for addr in addresses:
        pprint(addr.__dict__)

    # Test AddressModifiedStub
    print("\n--- Original and Modified Address ---")
    original = AddressStub()
    print("Original:")
    pprint(original.__dict__)

    modified = AddressModifiedStub.create_different(original)
    print("Modified:")
    pprint(modified.__dict__)
