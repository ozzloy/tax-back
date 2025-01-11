from http import HTTPStatus as http

from app.schema import StateSchema
from tests.stub import KingSignupStub


def test_king_create_success(client):
    """test successful king create with valid csrf token"""
    king_signup_data = KingSignupStub()

    response = client.post(
        "/api/king/",
        json=king_signup_data,
    )

    assert response.status_code == http.CREATED

    state = response.json
    assert "king" in state
    StateSchema(**state)


def test_king_create_failure_missing_csrf(client):
    """test that king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=KingSignupStub(),
        headers={"X-CSRF-TOKEN": None},
    )

    assert response.status_code == http.FORBIDDEN


def test_king_create_failure_invalid_csrf(client):
    """test king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=KingSignupStub(),
        headers={"X-CSRF-TOKEN": "invalid-csrf-token"},
    )

    assert response.status_code == http.FORBIDDEN


def test_king_create_missing_fields(client):
    """test king creation fails with missing field"""
    # Test missing all required fields
    response = client.post("/api/king/", json={})
    assert response.status_code == http.UNPROCESSABLE_ENTITY
    assert "errors" in response.json
    required_fields = ["email", "nick", "password"]
    errors = response.json["errors"]
    assert all(
        field in response.json["errors"] for field in required_fields
    )

    # Test missing individual fields
    for missing_field in required_fields:
        data = KingSignupStub()
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
                **KingSignupStub(),
                "email": "invalid-email",
            },
        },
        {
            "data": {
                **KingSignupStub(),
                "nick": "",
            },
        },
        {
            "data": {
                **KingSignupStub(),
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
    first_king_data = KingSignupStub()
    client.post("/api/king/", json=first_king_data)

    # attempt to create king with same email
    conflict_email_data = KingSignupStub()
    conflict_email_data["email"] = first_king_data["email"]

    response = client.post("/api/king/", json=conflict_email_data)
    assert response.status_code == 409
    assert response.json["message"] == "account conflict"
    assert "email is taken" in response.json["errors"]["email"]

    # attempt to create king with same nick
    conflict_nick_data = KingSignupStub()
    conflict_nick_data["nick"] = first_king_data["nick"]

    response = client.post("/api/king/", json=conflict_nick_data)
    assert response.status_code == 409
    assert response.json["message"] == "account conflict"
    assert "nick is taken" in response.json["errors"]["nick"]
