from http import HTTPStatus as http

from app.schema import SessionLoginSchema, StateSchema
from tests.stub import KingSignupStub


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
    assert list(state.keys()) == ["current_king"]
    StateSchema(**state)
