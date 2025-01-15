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


def test_form_1040_update_all_fields(logged_in_king):
    """test successful form_1040 update with all fields."""
    client, king = logged_in_king
    original_data = Form1040Stub().model_dump()

    create_response = client.post(
        "/api/form_1040/", json=original_data
    )
    state = create_response.json
    form_1040_slice = state["form_1040"]
    form_1040_id = next(iter(form_1040_slice.keys()))
    form_1040 = form_1040_slice[str(form_1040_id)]

    updated_data = Form1040ModifiedStub.create_different(
        original_data
    ).model_dump()
    updated_response = client.put(
        f"/api/form_1040/{form_1040_id}", json=updated_data
    )
    updated_state = updated_response.json
    updated_form_1040_slice = updated_state["form_1040"]
    updated_form_1040_id = next(iter(updated_form_1040_slice.keys()))
    updated_form_1040 = updated_form_1040_slice[
        str(updated_form_1040_id)
    ]

    # make sure unchangeable fields did not change
    assert updated_form_1040["id"] == form_1040["id"]
    assert updated_form_1040["created"] == form_1040["created"]
    assert updated_form_1040["king_id"] == form_1040["king_id"]

    # make sure changed fields have new values
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

    # TODO ensure filer, spouse, address are all None before
    assert "filer" not in updated_form_1040
    assert "spouse" not in updated_form_1040
    assert "address" not in updated_form_1040

    # TODO create filer, spouse, address and fill and check their ids
    filer_data = HumanStub().model_dump()
    spouse_data = HumanStub().model_dump()
    address_data = AddressStub().model_dump()
    response = client.post("/api/human/", json=filer_data)
    filer = next(iter(response.json["human"].values()))
    response = client.post("/api/human/", json=spouse_data)
    spouse = next(iter(response.json["human"].values()))
    response = client.post("/api/address/", json=address_data)
    address = next(iter(response.json["address"].values()))

    form_1040["filer_id"] = filer["id"]
    form_1040["spouse_id"] = spouse["id"]
    form_1040["address_id"] = address["id"]

    response = client.put(
        f"/api/form_1040/{form_1040['id']}", json=form_1040
    )
    updated0_form_1040 = list(response.json["form_1040"].values())[0]

    assert updated0_form_1040["filer_id"] == filer["id"]
    assert updated0_form_1040["spouse_id"] == spouse["id"]
    assert updated0_form_1040["address_id"] == address["id"]

    assert (
        updated_form_1040["updated"] < updated0_form_1040["updated"]
    )

    # TODO create updated filer, spouse, address and fill and check
    # their ids
    filer_data = HumanStub().model_dump()
    spouse_data = HumanStub().model_dump()
    address_data = AddressStub().model_dump()
    response = client.post("/api/human/", json=filer_data)
    new_filer = next(iter(response.json["human"].values()))
    response = client.post("/api/human/", json=spouse_data)
    new_spouse = next(iter(response.json["human"].values()))
    response = client.post("/api/address/", json=address_data)
    new_address = next(iter(response.json["address"].values()))

    form_1040["filer_id"] = new_filer["id"]
    form_1040["spouse_id"] = new_spouse["id"]
    form_1040["address_id"] = new_address["id"]

    response = client.put(
        f"/api/form_1040/{form_1040['id']}", json=form_1040
    )
    updated1_form_1040 = list(response.json["form_1040"].values())[0]

    assert updated1_form_1040["filer_id"] == new_filer["id"]
    assert updated1_form_1040["spouse_id"] == new_spouse["id"]
    assert updated1_form_1040["address_id"] == new_address["id"]

    assert (
        updated0_form_1040["updated"] < updated1_form_1040["updated"]
    )
    #


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
