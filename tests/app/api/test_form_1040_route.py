from http import HTTPStatus as http

from app.model import Form1040
from app.schema import StatePartialSchema
from app.stub import (
    AddressStub,
    Form1040ModifiedStub,
    Form1040Stub,
    HumanStub,
)

######################################################################
# create
######################################################################


def test_form_1040_create_success(logged_in_king):
    """Test successful creation of a form_1040 for a king"""

    client, king = logged_in_king
    form_1040_data = Form1040Stub().model_dump()

    create_response = client.post(
        "/api/form_1040/", json=form_1040_data
    )

    assert create_response.status_code == http.CREATED

    partial_state = create_response.json
    StatePartialSchema(**partial_state)

    assert "form_1040" in partial_state

    form_1040 = next(iter(partial_state["form_1040"].values()))

    assert form_1040["king_id"] == king["id"]


def test_form_1040_create_invalid_fields(logged_in_king):
    """Test unsuccessful form_1040 creation due to invalid data."""
    client, king_data = logged_in_king

    invalid_data_cases = [
        {
            "data": Form1040Stub().model_dump(),
            "invalid_field": "name",
            "invalid_value": "~",
        },
        {
            "data": Form1040Stub().model_dump(),
            "invalid_field": "tax_year",
            "invalid_value": 1912,
        },
        {
            "data": Form1040Stub().model_dump(),
            "invalid_field": "wages",
            "invalid_value": -1,
        },
        {
            "data": Form1040Stub().model_dump(),
            "invalid_field": "withholdings",
            "invalid_value": -1,
        },
        {
            "data": Form1040Stub().model_dump(),
            "invalid_field": "filing_status",
            "invalid_value": "this is not a filing status",
        },
    ]

    for test_case in invalid_data_cases:
        data = test_case["data"]
        invalid_field = test_case["invalid_field"]
        invalid_value = test_case["invalid_value"]
        data[invalid_field] = invalid_value
        response = client.post("/api/form_1040/", json=data)
        assert response.status_code == http.UNPROCESSABLE_ENTITY
        json = response.json
        assert json["message"] == "validation error"

        errors = json["errors"]
        assert invalid_field in errors
        valid_fields = list(data.keys())
        valid_fields.remove(invalid_field)
        assert all(field not in errors for field in valid_fields)


######################################################################
# read
######################################################################


def test_form_1040_read_all(logged_in_king):
    """test successful read of all form_1040s"""
    # make a request to read
    client, king = logged_in_king
    response_prior = client.get("/api/form_1040/")
    form_1040_data = Form1040Stub().model_dump()
    create_response = client.post(
        "/api/form_1040/", json=form_1040_data
    )
    response_post = client.get("/api/form_1040/")

    # assert that response_post contains everything from response_prior
    for form_1040_id, form_1040_data in response_prior.json[
        "form_1040"
    ].items():
        assert form_1040_id in response_post.json["form_1040"]
        assert (
            response_post.json["form_1040"][form_1040_id]
            == form_1040_data
        )

    # assert that response_post contains the newly created form_1040
    new_form_1040_id = list(create_response.json["form_1040"].keys())[
        0
    ]
    assert new_form_1040_id in response_post.json["form_1040"]
    assert (
        response_post.json["form_1040"][new_form_1040_id]
        == create_response.json["form_1040"][new_form_1040_id]
    )

    # verify the total number of form_1040s is correct
    assert (
        len(response_post.json["form_1040"])
        == len(response_prior.json["form_1040"]) + 1
    )


def test_form_1040_read(logged_in_king):
    """test successful read of all form_1040s"""
    # make a request to read
    client, king = logged_in_king
    form_1040_data = Form1040Stub().model_dump()
    create_response = client.post(
        "/api/form_1040/", json=form_1040_data
    )

    form_1040_id = next(
        iter(create_response.json["form_1040"].keys())
    )

    read_response = client.get(f"/api/form_1040/{form_1040_id}")
    assert read_response.status_code == http.OK
    assert create_response.json == read_response.json


######################################################################
# update
######################################################################


def test_form_1040_update_basic_fields(logged_in_king):
    """Test updating basic form 1040 fields like name, wages, etc."""
    client, king = logged_in_king
    original_data = Form1040Stub().model_dump()

    # create initial form
    create_response = client.post(
        "/api/form_1040/", json=original_data
    )
    form_1040_slice = create_response.json["form_1040"]
    form_1040_id = list(form_1040_slice.keys())[0]
    form_1040 = form_1040_slice[str(form_1040_id)]

    # update with new data
    updated_data = Form1040ModifiedStub.create_different(
        original_data
    ).model_dump()
    updated_response = client.put(
        f"/api/form_1040/{form_1040_id}", json=updated_data
    )
    updated_form_1040 = list(
        updated_response.json["form_1040"].values()
    )[0]

    # verify basic field updates
    assert updated_form_1040["name"] == updated_data["name"]
    assert updated_form_1040["wages"] == updated_data["wages"]
    assert (
        updated_form_1040["withholdings"]
        == updated_data["withholdings"]
    )
    assert (
        updated_form_1040["filing_status"]
        == updated_data["filing_status"]
    )
    assert form_1040["updated"] < updated_form_1040["updated"]


def test_form_1040_immutable_fields(logged_in_king):
    """Test that immutable fields stay static on update."""
    client, king = logged_in_king
    original_data = Form1040Stub().model_dump()

    # create initial form
    create_response = client.post(
        "/api/form_1040/", json=original_data
    )
    form_1040_slice = create_response.json["form_1040"]
    form_1040_id = next(iter(form_1040_slice.keys()))
    form_1040 = form_1040_slice[str(form_1040_id)]

    # update with new data
    updated_data = Form1040ModifiedStub.create_different(
        original_data
    ).model_dump()
    updated_response = client.put(
        f"/api/form_1040/{form_1040_id}", json=updated_data
    )
    updated_form_1040 = list(
        updated_response.json["form_1040"].values()
    )[0]

    # verify immutable fields
    assert updated_form_1040["id"] == form_1040["id"]
    assert updated_form_1040["created"] == form_1040["created"]
    assert updated_form_1040["king_id"] == form_1040["king_id"]


def test_form_1040_initial_relationships(logged_in_king):
    """Test that new form 1040 has no relationships set."""
    client, king = logged_in_king
    original_data = Form1040Stub().model_dump()

    # create initial form
    create_response = client.post(
        "/api/form_1040/", json=original_data
    )
    form_1040 = list(create_response.json["form_1040"].values())[0]

    # verify no relationships exist
    assert "filer" not in form_1040
    assert "spouse" not in form_1040
    assert "address" not in form_1040


def test_form_1040_add_relationships(logged_in_king):
    """Test adding filer, spouse, address to form 1040."""
    client, king = logged_in_king

    # create initial form
    original_data = Form1040Stub().model_dump()
    create_response = client.post(
        "/api/form_1040/", json=original_data
    )
    form_1040 = list(create_response.json["form_1040"].values())[0]

    # create related entities
    filer_data = HumanStub().model_dump()
    spouse_data = HumanStub().model_dump()
    address_data = AddressStub().model_dump()

    filer = list(
        client.post("/api/human/", json=filer_data)
        .json["human"]
        .values()
    )[0]
    spouse = list(
        client.post("/api/human/", json=spouse_data)
        .json["human"]
        .values()
    )[0]
    address = list(
        client.post("/api/address/", json=address_data)
        .json["address"]
        .values()
    )[0]

    # update form with relationships
    form_1040["filer_id"] = filer["id"]
    form_1040["spouse_id"] = spouse["id"]
    form_1040["address_id"] = address["id"]

    response = client.put(
        f"/api/form_1040/{form_1040['id']}", json=form_1040
    )
    updated_form_1040 = list(response.json["form_1040"].values())[0]

    # verify relationships
    assert updated_form_1040["filer_id"] == filer["id"]
    assert updated_form_1040["spouse_id"] == spouse["id"]
    assert updated_form_1040["address_id"] == address["id"]
    assert form_1040["updated"] < updated_form_1040["updated"]


def test_form_1040_update_relationships(logged_in_king):
    """Test updating existing relationship fields with new entities."""
    client, king = logged_in_king

    # create and setup initial form with relationships
    original_data = Form1040Stub().model_dump()
    create_response = client.post(
        "/api/form_1040/", json=original_data
    )
    form_1040 = list(create_response.json["form_1040"].values())[0]

    # create initial related entities
    filer = list(
        client.post("/api/human/", json=HumanStub().model_dump())
        .json["human"]
        .values()
    )[0]
    spouse = list(
        client.post("/api/human/", json=HumanStub().model_dump())
        .json["human"]
        .values()
    )[0]
    address = list(
        client.post("/api/address/", json=AddressStub().model_dump())
        .json["address"]
        .values()
    )[0]

    # set initial relationships
    form_1040["filer_id"] = filer["id"]
    form_1040["spouse_id"] = spouse["id"]
    form_1040["address_id"] = address["id"]

    initial_update = client.put(
        f"/api/form_1040/{form_1040['id']}", json=form_1040
    )
    form_1040_with_relations = list(
        initial_update.json["form_1040"].values()
    )[0]

    # create new related entities
    new_filer = list(
        client.post("/api/human/", json=HumanStub().model_dump())
        .json["human"]
        .values()
    )[0]
    new_spouse = list(
        client.post("/api/human/", json=HumanStub().model_dump())
        .json["human"]
        .values()
    )[0]
    new_address = list(
        client.post("/api/address/", json=AddressStub().model_dump())
        .json["address"]
        .values()
    )[0]

    # update with new relationships
    form_1040_with_relations["filer_id"] = new_filer["id"]
    form_1040_with_relations["spouse_id"] = new_spouse["id"]
    form_1040_with_relations["address_id"] = new_address["id"]

    final_response = client.put(
        f"/api/form_1040/{form_1040_with_relations['id']}",
        json=form_1040_with_relations,
    )
    final_form_1040 = list(final_response.json["form_1040"].values())[
        0
    ]

    # verify updated relationships
    assert final_form_1040["filer_id"] == new_filer["id"]
    assert final_form_1040["spouse_id"] == new_spouse["id"]
    assert final_form_1040["address_id"] == new_address["id"]
    assert (
        form_1040_with_relations["updated"]
        < final_form_1040["updated"]
    )


######################################################################
# delete
######################################################################


def test_form_1040_delete_removes_from_db(logged_in_king, test_db):
    """test that form_1040 deletion really deletes record from db."""

    client, king_data = logged_in_king
    form_1040_data = Form1040Stub().model_dump()

    create_response = client.post(
        "/api/form_1040/", json=form_1040_data
    )
    state = create_response.json
    form_1040_slice = state["form_1040"]
    form_1040_id = next(iter(form_1040_slice.keys()))
    # create_form_1040 = form_1040_slice[str(form_1040_id)]

    # check the db to see if table "form_1040" has the record
    db_form_1040 = test_db.session.get(Form1040, form_1040_id)
    assert db_form_1040

    delete_response = client.delete(f"/api/form_1040/{form_1040_id}")
    delete_state = delete_response.json
    delete_form_1040_slice = delete_state["form_1040"]
    delete_form_1040_id = next(iter(delete_form_1040_slice.keys()))
    delete_form_1040 = delete_form_1040_slice[
        str(delete_form_1040_id)
    ]

    assert delete_form_1040 is None
    assert delete_form_1040_id == form_1040_id

    deleted_form_1040 = test_db.session.get(Form1040, form_1040_id)
    assert deleted_form_1040 is None
