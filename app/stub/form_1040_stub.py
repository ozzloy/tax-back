"""generate form_1040s."""

import random
from datetime import datetime

import factory
from app.schema import Form1040InputSchema
from app.schema.form_1040_schema import filing_statuses
from faker import Faker

fake = Faker()


class Form1040Stub(factory.Factory):
    """Generate form_1040 creation data."""

    class Meta:
        """The meta class for form_1040 factory."""

        model = Form1040InputSchema

    name = factory.LazyAttribute(lambda _: fake.bs())
    tax_year = factory.LazyAttribute(
        lambda _: random.randint(1913, datetime.now().year + 1)
    )
    # not generating foreign keys, they must be generated once
    # there are records with real ids to go with them
    # filer_id = factory.LazyAttribute(lambda _: random.randint())
    # spouse_id
    # address_id

    wages = factory.LazyAttribute(
        lambda _: random.uniform(1000, 24_000_000_000)
    )

    withholdings = factory.LazyAttribute(
        lambda _: random.uniform(0, 1000)
    )

    filing_status = random.choice(filing_statuses)


class Form1040ModifiedStub(Form1040Stub):
    """Generate different form_1040 data from an original form_1040."""

    @classmethod
    def create_different(cls, original_data):
        """Create form_1040 ensuring all fields have new values."""
        unique_fake = Faker()

        unique_fake.unique.exclude_bs = {original_data["name"]}
        different_name = unique_fake.unique.bs()

        different_year = random.randint(1913, datetime.now().year + 1)
        while different_year == original_data["tax_year"]:
            different_year = random.randint(
                1913, datetime.now().year + 1
            )

        different_wages = random.uniform(1000, 24_000_000_000)
        while different_wages == original_data["wages"]:
            different_wages = random.uniform(1000, 24_000_000_000)

        different_withholdings = random.uniform(0, 1000)
        while different_withholdings == original_data["withholdings"]:
            different_withholdings = random.uniform(0, 1000)

        different_status = random.choice(filing_statuses)
        while different_status == original_data["filing_status"]:
            different_status = random.choice(filing_statuses)

        return Form1040InputSchema(
            name=different_name,
            tax_year=different_year,
            wages=different_wages,
            withholdings=different_withholdings,
            filing_status=different_status,
        )


# Test script
if __name__ == "__main__":
    """
    run from tax directory like this:
    $ PYTHONPATH="." pipenv run python app/stub/form_1040_stub.py
    """
    from pprint import pprint

    # Generate a random form_1040 using Form1040Stub
    print("--- Generated Random Form_1040 ---")
    random_form_1040 = Form1040Stub()
    pprint(random_form_1040.__dict__)

    # Generate multiple form_1040es
    print("\n--- Multiple Random Form_1040es ---")
    form_1040s = [Form1040Stub() for _ in range(3)]
    for addr in form_1040s:
        pprint(addr.__dict__)

    # Test Form1040ModifiedStub
    print("\n--- Original and Modified Form_1040 ---")
    original = Form1040Stub()
    print("Original:")
    pprint(original.__dict__)

    modified = Form1040ModifiedStub.create_different(
        original.model_dump()
    )
    print("Modified:")
    pprint(modified.__dict__)
