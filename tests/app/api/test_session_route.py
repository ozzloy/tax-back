from http import HTTPStatus as http

from app.schema import SessionLoginSchema, StatePartialSchema
from app.stub import KingStub, SessionLoginStub


def test_session_create_success(client):
    king_signup_data = KingStub().model_dump()
    client.post("/api/king/", json=king_signup_data)
    session_login_data = SessionLoginSchema(
        **king_signup_data
    ).model_dump()
    login_response = client.post(
        "/api/session/", json=session_login_data
    )
    assert login_response.status_code == http.OK

    state = login_response.json
    StatePartialSchema(**state)


def test_session_create_missing_fields(client):
    """test login failure when fields are missing."""
    # test empty object, all fields missing
    response = client.post("/api/session/", json={})
    assert response.status_code == http.UNPROCESSABLE_ENTITY
    assert "errors" in response.json
    errors = response.json["errors"]
    required_fields = SessionLoginSchema.model_fields
    assert all(field in errors for field in required_fields)

    # test individual fields missing
    for missing_field in required_fields:
        data = SessionLoginStub().model_dump()
        del data[missing_field]

        response = client.post("/api/session/", json=data)

        assert response.status_code == http.UNPROCESSABLE_ENTITY
        assert response.json["message"] == "validation error"
        errors = response.json["errors"]
        assert missing_field in errors
        for key in data:
            assert key not in errors


def test_session_create_validation_error(client):
    """test login validation failure."""
    invalid_data = {
        "email": "invalid-email",
        "password": "",
    }

    response = client.post("/api/session/", json=invalid_data)
    assert response.status_code == http.UNPROCESSABLE_ENTITY
    assert response.json["message"] == "validation error"
    assert "email" in response.json["errors"]
    assert "password" in response.json["errors"]


def test_session_create_invalid_login(client):
    """test failures occuring from invalid credentials"""
    # test completely new user
    nonextant_login = {
        "email": "nonextant@example.org",
        "password": "at least 6 characters",
    }
    response = client.post("/api/session/", json=nonextant_login)
    assert response.status_code == http.UNAUTHORIZED
    assert response.json["message"] == "invalid credentials"

    king_signup_data = KingStub().model_dump()
    client.post("/api/king/", json=king_signup_data)
    login_data = SessionLoginSchema(**king_signup_data).model_dump()
    wrong_password = login_data["password"] + "a"
    login_wrong_password = login_data | {"password": wrong_password}
    wrong_password_response = client.post(
        "/api/session/", json=login_wrong_password
    )

    assert wrong_password_response.status_code == http.UNAUTHORIZED


def test_session_delete_success(client):
    """test successful logout."""
    # first login
    king_signup_data = KingStub().model_dump()
    client.post("/api/king/", json=king_signup_data)
    session_login_data = SessionLoginSchema(
        **king_signup_data
    ).model_dump()
    login_response = client.post(
        "/api/session/", json=session_login_data
    )
    state = login_response.json
    king_slice = state["king"]
    king_id = state["current_king_id"]
    king = king_slice[str(king_id)]

    # then logout
    delete_response = client.delete("/api/session/")

    # verify response
    assert delete_response.status_code == http.OK
    delete_state = delete_response.json

    assert delete_state["current_king_id"] is None

    delete_king_slice = delete_state["king"]
    delete_king = delete_king_slice[str(king_id)]

    assert delete_king["nick"] == king["nick"]
    assert delete_king["id"] == king["id"]

    # attempt an unauthorized read
    read_response = client.get("/api/king/")
    # expect it to fail
    assert read_response.status_code == http.UNAUTHORIZED


def test_session_delete_when_not_logged_in(client):
    """test logout when no session exists returns successfully."""
    response = client.delete("/api/session/")
    assert response.status_code == http.NO_CONTENT
