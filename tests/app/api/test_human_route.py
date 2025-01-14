from http import HTTPStatus as http

from app.model import Human
from app.schema import StatePartialSchema
from app.stub import DifferentHumanStub, HumanStub

######################################################################
# create
######################################################################


def test_human_create_success(logged_in_king):
    """Test successful creation of a human for a king"""
    client, king = logged_in_king
    human_data = HumanStub().model_dump()
    create_response = client.post("/api/human/", json=human_data)

    assert create_response.status_code == http.CREATED

    partial_state = create_response.json
    StatePartialSchema(**partial_state)

    assert "human" in partial_state

    human = next(iter(partial_state["human"].values()))

    assert human["king_id"] == king["id"]


def test_human_create_invalid_fields(logged_in_king):
    """Test unsuccessful human creation due to invalid human data."""
    client, king_data = logged_in_king

    invalid_data_cases = [
        {
            "data": HumanStub().model_dump(),
            "invalid_field": "first_name",
            "invalid_value": "",
        },
        {
            "data": HumanStub().model_dump(),
            "invalid_field": "middle_initial",
            "invalid_value": "not a web color",
        },
        {
            "data": HumanStub().model_dump(),
            "invalid_field": "last_name",
            "invalid_value": "",
        },
    ]

    for test_case in invalid_data_cases:
        data = test_case["data"]
        invalid_field = test_case["invalid_field"]
        invalid_value = test_case["invalid_value"]
        data[invalid_field] = invalid_value
        response = client.post("/api/human/", json=data)
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


def test_human_read_all(logged_in_king):
    """test successful read of all humans"""
    # make a request to read
    client, king = logged_in_king
    response_prior = client.get("/api/human/")
    human_data = HumanStub().model_dump()
    create_response = client.post("/api/human/", json=human_data)
    response_post = client.get("/api/human/")

    # assert that response_post contains everything from response_prior
    for human_id, human_data in response_prior.json["human"].items():
        assert human_id in response_post.json["human"]
        assert response_post.json["human"][human_id] == human_data

    # assert that response_post contains the newly created human
    new_human_id = list(create_response.json["human"].keys())[0]
    assert new_human_id in response_post.json["human"]
    assert (
        response_post.json["human"][new_human_id]
        == create_response.json["human"][new_human_id]
    )

    # verify the total number of humans is correct
    assert (
        len(response_post.json["human"])
        == len(response_prior.json["human"]) + 1
    )


def test_human_read(logged_in_king):
    """test successful read of all humans"""
    # make a request to read
    client, king = logged_in_king
    human_data = HumanStub().model_dump()
    create_response = client.post("/api/human/", json=human_data)

    human_id = next(iter(create_response.json["human"].keys()))

    read_response = client.get(f"/api/human/{human_id}")
    assert read_response.status_code == http.OK
    assert create_response.json == read_response.json


######################################################################
# update
######################################################################


def test_human_update_all_fields(logged_in_king):
    """test successful human update with all fields."""
    client, king = logged_in_king
    original_data = HumanStub().model_dump()

    create_response = client.post("/api/human/", json=original_data)
    state = create_response.json
    human_slice = state["human"]
    human_id = next(iter(human_slice.keys()))
    human = human_slice[str(human_id)]

    updated_data = DifferentHumanStub.create_different(
        original_data
    ).model_dump()
    updated_response = client.put(
        f"/api/human/{human_id}", json=updated_data
    )
    updated_state = updated_response.json
    updated_human_slice = updated_state["human"]
    updated_human_id = next(iter(updated_human_slice.keys()))
    updated_human = updated_human_slice[str(updated_human_id)]

    # make sure unchangeable fields did not change
    assert updated_human["id"] == human["id"]
    assert updated_human["created"] == human["created"]
    assert updated_human["king_id"] == human["king_id"]

    # make sure changed fields have new values
    assert updated_human["first_name"] == updated_data["first_name"]
    assert updated_human["last_name"] == updated_data["last_name"]
    assert (
        updated_human["middle_initial"]
        == updated_data["middle_initial"]
    )

    assert human["updated"] < updated_human["updated"]


######################################################################
# delete
######################################################################


def test_human_delete_removes_from_db(logged_in_king, test_db):
    """test that human deletion really deletes record from database."""

    client, king_data = logged_in_king
    human_data = HumanStub().model_dump()

    create_response = client.post("/api/human/", json=human_data)
    state = create_response.json
    human_slice = state["human"]
    human_id = next(iter(human_slice.keys()))
    # create_human = human_slice[str(human_id)]

    # check the db to see if table "human" has the record
    db_human = test_db.session.get(Human, human_id)
    assert db_human

    delete_response = client.delete(f"/api/human/{human_id}")
    delete_state = delete_response.json
    delete_human_slice = delete_state["human"]
    delete_human_id = next(iter(delete_human_slice.keys()))
    delete_human = delete_human_slice[str(delete_human_id)]

    assert delete_human is None
    assert delete_human_id == human_id

    deleted_human = test_db.session.get(Human, human_id)
    assert deleted_human is None
