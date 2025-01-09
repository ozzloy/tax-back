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
