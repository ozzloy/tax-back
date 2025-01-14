from http import HTTPStatus as http

from app.model import Address
from app.schema import StatePartialSchema
from app.stub import AddressModifiedStub, AddressStub

######################################################################
# create
######################################################################


def test_address_create_success(logged_in_king):
    """Test successful creation of a address for a king"""

    client, king = logged_in_king
    address_data = AddressStub().model_dump()

    create_response = client.post("/api/address/", json=address_data)

    assert create_response.status_code == http.CREATED

    partial_state = create_response.json
    StatePartialSchema(**partial_state)

    assert "address" in partial_state

    address = next(iter(partial_state["address"].values()))

    assert address["king_id"] == king["id"]


def test_address_create_invalid_fields(logged_in_king):
    """Test unsuccessful address creation due to invalid address data."""
    client, king_data = logged_in_king

    invalid_data_cases = [
        {
            "data": AddressStub().model_dump(),
            "invalid_field": "street",
            "invalid_value": "&(*)",
        },
        {
            "data": AddressStub().model_dump(),
            "invalid_field": "city",
            "invalid_value": "***!!",
        },
        {
            "data": AddressStub().model_dump(),
            "invalid_field": "state",
            "invalid_value": "ca",
        },
        {
            "data": AddressStub().model_dump(),
            "invalid_field": "zip",
            "invalid_value": "abcde",
        },
    ]

    for test_case in invalid_data_cases:
        data = test_case["data"]
        invalid_field = test_case["invalid_field"]
        invalid_value = test_case["invalid_value"]
        data[invalid_field] = invalid_value
        response = client.post("/api/address/", json=data)
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


def test_address_read_all(logged_in_king):
    """test successful read of all addresss"""
    # make a request to read
    client, king = logged_in_king
    response_prior = client.get("/api/address/")
    address_data = AddressStub().model_dump()
    create_response = client.post("/api/address/", json=address_data)
    response_post = client.get("/api/address/")

    # assert that response_post contains everything from response_prior
    for address_id, address_data in response_prior.json[
        "address"
    ].items():
        assert address_id in response_post.json["address"]
        assert (
            response_post.json["address"][address_id] == address_data
        )

    # assert that response_post contains the newly created address
    new_address_id = list(create_response.json["address"].keys())[0]
    assert new_address_id in response_post.json["address"]
    assert (
        response_post.json["address"][new_address_id]
        == create_response.json["address"][new_address_id]
    )

    # verify the total number of addresss is correct
    assert (
        len(response_post.json["address"])
        == len(response_prior.json["address"]) + 1
    )


def test_address_read(logged_in_king):
    """test successful read of all addresss"""
    # make a request to read
    client, king = logged_in_king
    address_data = AddressStub().model_dump()
    create_response = client.post("/api/address/", json=address_data)

    address_id = next(iter(create_response.json["address"].keys()))

    read_response = client.get(f"/api/address/{address_id}")
    assert read_response.status_code == http.OK
    assert create_response.json == read_response.json


######################################################################
# update
######################################################################


def test_address_update_all_fields(logged_in_king):
    """test successful address update with all fields."""
    client, king = logged_in_king
    original_data = AddressStub().model_dump()

    create_response = client.post("/api/address/", json=original_data)
    state = create_response.json
    address_slice = state["address"]
    address_id = next(iter(address_slice.keys()))
    address = address_slice[str(address_id)]

    updated_data = AddressModifiedStub.create_different(
        original_data
    ).model_dump()
    updated_response = client.put(
        f"/api/address/{address_id}", json=updated_data
    )
    updated_state = updated_response.json
    updated_address_slice = updated_state["address"]
    updated_address_id = next(iter(updated_address_slice.keys()))
    updated_address = updated_address_slice[str(updated_address_id)]

    # make sure unchangeable fields did not change
    assert updated_address["id"] == address["id"]
    assert updated_address["created"] == address["created"]
    assert updated_address["king_id"] == address["king_id"]

    # make sure changed fields have new values
    assert updated_address["street"] == updated_data["street"]
    assert updated_address["city"] == updated_data["city"]
    assert updated_address["state"] == updated_data["state"]
    assert updated_address["zip"] == updated_data["zip"]

    assert address["updated"] < updated_address["updated"]


######################################################################
# delete
######################################################################


def test_address_delete_removes_from_db(logged_in_king, test_db):
    """test that address deletion really deletes record from database."""

    client, king_data = logged_in_king
    address_data = AddressStub().model_dump()

    create_response = client.post("/api/address/", json=address_data)
    state = create_response.json
    address_slice = state["address"]
    address_id = next(iter(address_slice.keys()))
    # create_address = address_slice[str(address_id)]

    # check the db to see if table "address" has the record
    db_address = test_db.session.get(Address, address_id)
    assert db_address

    delete_response = client.delete(f"/api/address/{address_id}")
    delete_state = delete_response.json
    delete_address_slice = delete_state["address"]
    delete_address_id = next(iter(delete_address_slice.keys()))
    delete_address = delete_address_slice[str(delete_address_id)]

    assert delete_address is None
    assert delete_address_id == address_id

    deleted_address = test_db.session.get(Address, address_id)
    assert deleted_address is None
