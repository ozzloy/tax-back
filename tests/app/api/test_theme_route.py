from http import HTTPStatus as http

from app.schema import StatePartialSchema
from tests.stub import ThemeCreateStub


def test_theme_create_success(logged_in_king):
    """Test successful creation of a theme for a king"""
    client, original_king_data = logged_in_king
    theme_data = ThemeCreateStub().model_dump()
    create_response = client.post("/api/theme/", json=theme_data)

    assert create_response.status_code == http.CREATED

    partial_state = create_response.json
    StatePartialSchema(**partial_state)
