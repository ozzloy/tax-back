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
    """test that king create fails when missing csrf token"""
    response = client.post(
        "/api/king/",
        json=factory.make_king_signup_data(),
        headers={"X-CSRF-TOKEN": "invalid-csrf-token"},
    )

    assert response.status_code == 400
