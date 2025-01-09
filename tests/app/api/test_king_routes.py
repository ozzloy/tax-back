from app.validator import king_validator
from tests import factory


def test_king_create_success(client):
    """test successful king create with valid csrf token"""
    response = client.post(
        "/api/king/",
        json=factory.make_king_signup_data(),
    )

    assert response.status_code == 201

    partial_state = response.json
    assert "king" in partial_state
    king_slice = partial_state["king"]
    king_validator.validate_king_slice(king_slice)


def test_king_create_failure_missing_csrf(client):
    """test that king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=factory.make_king_signup_data(),
        headers={"X-CSRF-TOKEN": None},
    )

    assert response.status_code == 400


def test_king_create_failure_invalid_csrf(client):
    """test king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=factory.make_king_signup_data(),
        headers={"X-CSRF-TOKEN": "invalid-csrf-token"},
    )

    assert response.status_code == 400


def test_king_create_missing_fields(client):
    """test king creation fails with missing field"""
    # Test missing all required fields
    required_fields = ["email", "nick", "password"]
    response = client.post("/api/king/", json={})
    assert response.status_code == 400
    assert "errors" in response.json
    assert all(
        field in response.json["errors"] for field in required_fields
    )

    # Test missing individual fields
    for missing_field in required_fields:
        data = factory.make_king_signup_data()
        del data[missing_field]

        response = client.post("/api/king/", json=data)
        assert response.status_code == 400
        assert response.json["message"] == "field missing"
        errors = response.json["errors"]
        assert missing_field in errors
        for key in data:
            assert key not in errors


def test_king_create_invalid_fields(client):
    """test king creation fails with invalid field values"""
    invalid_data_cases = [
        {
            "data": {
                **factory.make_king_signup_data(),
                "email": "invalid-email",
            },
            "expected_error": "invalid email",
        },
        {
            "data": {**factory.make_king_signup_data(), "nick": ""},
            "expected_error": "nick must have at least 1 character",
        },
        {
            "data": {
                **factory.make_king_signup_data(),
                "password": "",
            },
            "expected_error": "password must have at least 1 character",
        },
    ]

    for test_case in invalid_data_cases:
        response = client.post("/api/king/", json=test_case["data"])
        assert response.status_code == 422
        assert response.json["message"] == "bad request"
        assert any(
            test_case["expected_error"] in error
            for error in response.json["errors"].values()
        )


def test_king_create_conflict(client):
    """test king creation fails when email or nick is already taken"""
    # create a king
    first_king_data = factory.make_king_signup_data()
    client.post("/api/king/", json=first_king_data)

    # attempt to create king with same email
    conflict_email_data = factory.make_king_signup_data()
    conflict_email_data["email"] = first_king_data["email"]

    response = client.post("/api/king/", json=conflict_email_data)
    assert response.status_code == 409
    assert response.json["message"] == "account conflict"
    assert "email is taken" in response.json["errors"]["email"]

    # attempt to create king with same nick
    conflict_nick_data = factory.make_king_signup_data()
    conflict_nick_data["nick"] = first_king_data["nick"]

    response = client.post("/api/king/", json=conflict_nick_data)
    assert response.status_code == 409
    assert response.json["message"] == "account conflict"
    assert "nick is taken" in response.json["errors"]["nick"]
