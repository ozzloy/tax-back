from app.schema import SessionLoginSchema
from tests.stub import KingSignupStub


def test_session_create_success(client):
    king_signup_data = KingSignupStub()
    client.post("/api/king/", json=king_signup_data)
    session_login_data = SessionLoginSchema(**king_signup_data)
    login_response = client.post(
        "/api/session/", json=session_login_data
    )
