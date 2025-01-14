from http import HTTPStatus as http

from app.model import King
from app.schema import KingSignupSchema, StatePartialSchema
from app.stub import KingStub

######################################################################
# create
######################################################################


def test_king_create_success(client):
    """test successful king create with valid csrf token"""
    king_signup_data = KingStub().model_dump()

    signup_response = client.post("/api/king/", json=king_signup_data)

    assert signup_response.status_code == http.CREATED

    partial_state = signup_response.json
    StatePartialSchema(**partial_state)


def test_king_create_failure_missing_csrf(client):
    """test that king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=KingStub().model_dump(),
        headers={"X-CSRF-TOKEN": None},
    )

    assert response.status_code == http.FORBIDDEN


def test_king_create_failure_invalid_csrf(client):
    """test king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=KingStub().model_dump(),
        headers={"X-CSRF-TOKEN": "invalid-csrf-token"},
    )

    assert response.status_code == http.FORBIDDEN


def test_king_create_missing_fields(client):
    """test king creation fails with missing field"""
    # test missing all required fields
    response = client.post("/api/king/", json={})
    assert response.status_code == http.UNPROCESSABLE_ENTITY
    assert "errors" in response.json
    errors = response.json["errors"]
    required_fields = KingSignupSchema.model_fields
    assert all(field in errors for field in required_fields)

    # test missing individual fields
    for missing_field in required_fields:
        data = KingStub().model_dump()
        del data[missing_field]

        response = client.post("/api/king/", json=data)

        assert response.status_code == http.UNPROCESSABLE_ENTITY
        assert response.json["message"] == "validation error"
        errors = response.json["errors"]
        assert missing_field in errors
        for key in data:
            assert key not in errors


def test_king_create_invalid_fields(client):
    """test king creation fails with invalid field values"""
    invalid_data_cases = [
        {
            "data": {
                **KingStub().model_dump(),
                "email": "invalid-email",
            },
        },
        {
            "data": {
                **KingStub().model_dump(),
                "nick": "",
            },
        },
        {
            "data": {
                **KingStub().model_dump(),
                "password": "",
            },
        },
    ]

    for test_case in invalid_data_cases:
        response = client.post("/api/king/", json=test_case["data"])
        assert response.status_code == http.UNPROCESSABLE_ENTITY
        assert response.json["message"] == "validation error"


def test_king_create_conflict(client):
    """test king creation fails when email or nick is already taken"""
    # create a king
    first_king_data = KingStub().model_dump()
    client.post("/api/king/", json=first_king_data)

    # attempt to create king with same email
    conflict_email_data = KingStub().model_dump()
    conflict_email_data["email"] = first_king_data["email"]

    response = client.post("/api/king/", json=conflict_email_data)
    assert response.status_code == 409
    assert response.json["message"] == "account conflict"
    assert "email is taken" in response.json["errors"]["email"]

    # attempt to create king with same nick
    conflict_nick_data = KingStub().model_dump()
    conflict_nick_data["nick"] = first_king_data["nick"]

    response = client.post("/api/king/", json=conflict_nick_data)
    assert response.status_code == 409
    assert response.json["message"] == "account conflict"
    assert "nick is taken" in response.json["errors"]["nick"]


######################################################################
# read
######################################################################


def test_king_read_logged_in(logged_in_king):
    client, king_data = logged_in_king

    read_response = client.get("/api/king/")
    state = read_response.json
    StatePartialSchema(**state)

    current_king_id = state["current_king_id"]
    current_king = state["king"][str(current_king_id)]
    assert "password" not in current_king
    del king_data["password"]

    for field in king_data:
        assert field in current_king

    for key, value in king_data.items():
        assert current_king[key] == value


def test_king_read_anonymous(client):
    read_response = client.get("/api/king/")
    assert read_response.status_code == http.UNAUTHORIZED


######################################################################
# update
######################################################################


def test_king_update_all_fields(logged_in_king):
    """test successful king update with all fields."""
    client, original_king_data = logged_in_king
    update_data = KingStub().model_dump()
    old_password = original_king_data["password"]
    new_password = update_data["password"]

    update_response = client.put("/api/king/", json=update_data)
    assert update_response.status_code == http.OK

    # validate response structure
    state = update_response.json
    StatePartialSchema(**state)

    # verify updated fields
    current_king_id = state["current_king_id"]
    updated_king = state["king"][str(current_king_id)]

    # password should not be returned
    assert "password" not in updated_king

    # check that fields were updated
    del update_data["password"]
    for key, value in update_data.items():
        assert updated_king[key] == value

    # log out
    client.delete("/api/session/")
    # try to log in with old password
    login_old_password_data = {
        "email": update_data["email"],
        "password": old_password,
    }
    old_password_response = client.post(
        "/api/session/", json=login_old_password_data
    )
    # assert that it fails
    assert old_password_response.status_code == http.UNAUTHORIZED
    # try to log in with new password
    login_new_password_data = {
        "email": update_data["email"],
        "password": new_password,
    }
    new_password_response = client.post(
        "/api/session/", json=login_new_password_data
    )
    # assert login with new password succeeds
    assert new_password_response.status_code == http.OK


def test_king_update_partial(logged_in_king):
    """test successful king update with only some fields."""

    client, original_king_data = logged_in_king
    update_data = {"email": "newemail@example.com"}

    update_response = client.put("/api/king/", json=update_data)
    assert update_response.status_code == http.OK

    state = update_response.json
    current_king_id = state["current_king_id"]
    updated_king = state["king"][str(current_king_id)]

    # check that specified field was updated
    assert updated_king["email"] == update_data["email"]

    # check that unspecified fields remain unchanged
    assert updated_king["nick"] == original_king_data["nick"]


def test_king_update_invalid_email(logged_in_king):
    """test king update with invalid email format."""
    client, _ = logged_in_king
    update_data = {"email": "invalid-email"}

    response = client.put("/api/king/", json=update_data)
    assert response.status_code == http.UNPROCESSABLE_ENTITY


def test_king_update_short_password(logged_in_king):
    """test king update with password that's too short."""
    client, _ = logged_in_king
    update_data = {"password": "short"}

    response = client.put("/api/king/", json=update_data)
    assert response.status_code == http.UNPROCESSABLE_ENTITY


def test_king_update_unauthenticated(client):
    """test king update without authentication."""
    update_data = KingStub().model_dump()

    response = client.put("/api/king/", json=update_data)
    assert response.status_code == http.UNAUTHORIZED


def test_king_update_empty_nick(logged_in_king):
    """test king update with empty nickname."""
    client, _ = logged_in_king
    update_data = {"nick": ""}

    response = client.put("/api/king/", json=update_data)
    assert response.status_code == http.UNPROCESSABLE_ENTITY


def test_king_update_invalid_theme(logged_in_king):
    """test king update with invalid theme_id."""
    client, _ = logged_in_king
    update_data = {"theme_id": -1}

    response = client.put("/api/king/", json=update_data)
    assert response.status_code == http.UNPROCESSABLE_ENTITY


######################################################################
# update
######################################################################


def test_king_delete_requires_auth(client):
    """test that king deletion requires authentication."""
    response = client.delete("/api/king/")
    assert response.status_code == http.UNAUTHORIZED


def test_king_delete_success(logged_in_king):
    """test successful king account deletion."""
    client, king_data = logged_in_king

    # first verify we can access the account
    get_response = client.get("/api/king/")
    assert get_response.status_code == http.OK

    # Delete the account
    delete_response = client.delete("/api/king/")
    assert delete_response.status_code == http.OK

    # verify response structure
    state = delete_response.json
    assert state == {"current_king_id": None}

    # verify we can no longer access the account
    get_response_after = client.get("/api/king/")
    assert get_response_after.status_code == http.UNAUTHORIZED

    # Verify we can't log in with the old credentials
    login_data = {
        "email": king_data["email"],
        "password": king_data["password"],
    }
    login_response = client.post("/api/session/", json=login_data)
    assert login_response.status_code == http.UNAUTHORIZED


def test_king_delete_removes_from_db(logged_in_king, test_db):
    """test that king deletion really deletes record from database."""

    client, king_data = logged_in_king
    king_id = king_data["id"]

    # delete the account
    delete_response = client.delete("/api/king/")
    assert delete_response.status_code == http.OK

    # verify king no longer exists in database
    deleted_king = test_db.session.get(King, king_id)
    assert deleted_king is None
