from http import HTTPStatus as http

from app.schema import SessionLoginSchema, StateSchema
from tests.stub import KingSignupStub, SessionLoginStub


def test_session_create_success(client):
    king_signup_data = KingSignupStub().model_dump()
    client.post("/api/king/", json=king_signup_data)
    session_login_data = SessionLoginSchema(
        **king_signup_data
    ).model_dump()
    login_response = client.post(
        "/api/session/", json=session_login_data
    )
    assert login_response.status_code == http.OK

    state = login_response.json
    StateSchema(**state)


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
