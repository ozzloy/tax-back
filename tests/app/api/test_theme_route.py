from http import HTTPStatus as http

from app.schema import StatePartialSchema
from tests.stub import ThemeCreateStub

######################################################################
# create
######################################################################


def test_theme_create_success(logged_in_king):
    """Test successful creation of a theme for a king"""
    client, king = logged_in_king
    theme_data = ThemeCreateStub().model_dump()
    create_response = client.post("/api/theme/", json=theme_data)

    assert create_response.status_code == http.CREATED

    partial_state = create_response.json
    StatePartialSchema(**partial_state)

    assert "theme" in partial_state

    theme = next(iter(partial_state["theme"].values()))

    assert theme["king_id"] == king["id"]


def test_theme_create_invalid_fields(logged_in_king):
    """Test unsuccessful theme creation due to invalid theme data."""
    client, king_data = logged_in_king

    invalid_data_cases = [
        {
            "data": ThemeCreateStub().model_dump(),
            "invalid_field": "name",
            "invalid_value": "",
        },
        {
            "data": ThemeCreateStub().model_dump(),
            "invalid_field": "text_color",
            "invalid_value": "not a web color",
        },
        {
            "data": ThemeCreateStub().model_dump(),
            "invalid_field": "background_color",
            "invalid_value": "still not a web color",
        },
    ]

    for test_case in invalid_data_cases:
        data = test_case["data"]
        invalid_field = test_case["invalid_field"]
        invalid_value = test_case["invalid_value"]
        data[invalid_field] = invalid_value
        response = client.post("/api/theme/", json=data)
        assert response.status_code == http.UNPROCESSABLE_ENTITY
        json = response.json
        assert json["message"] == "validation error"

        errors = json["errors"]
        assert invalid_field in errors
        valid_fields = list(data.keys())
        valid_fields.remove(invalid_field)
        assert all(field not in errors for field in valid_fields)


######################################################################
# read
######################################################################


def test_theme_read_all(logged_in_king):
    """test successful read of all themes"""
    # make a request to read
    client, king = logged_in_king
    response_prior = client.get("/api/theme/")
    theme_data = ThemeCreateStub().model_dump()
    create_response = client.post("/api/theme/", json=theme_data)
    response_post = client.get("/api/theme/")

    # assert that response_post contains everything from response_prior
    for theme_id, theme_data in response_prior.json["theme"].items():
        assert theme_id in response_post.json["theme"]
        assert response_post.json["theme"][theme_id] == theme_data

    # assert that response_post contains the newly created theme
    new_theme_id = list(create_response.json["theme"].keys())[0]
    assert new_theme_id in response_post.json["theme"]
    assert (
        response_post.json["theme"][new_theme_id]
        == create_response.json["theme"][new_theme_id]
    )

    # verify the total number of themes is correct
    assert (
        len(response_post.json["theme"])
        == len(response_prior.json["theme"]) + 1
    )
