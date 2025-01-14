from http import HTTPStatus as http

from app.model import Theme
from app.schema import StatePartialSchema
from app.stub import ThemeStub

######################################################################
# create
######################################################################


def test_theme_create_success(logged_in_king):
    """Test successful creation of a theme for a king"""
    client, king = logged_in_king
    theme_data = ThemeStub().model_dump()
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
            "data": ThemeStub().model_dump(),
            "invalid_field": "name",
            "invalid_value": "",
        },
        {
            "data": ThemeStub().model_dump(),
            "invalid_field": "text_color",
            "invalid_value": "not a web color",
        },
        {
            "data": ThemeStub().model_dump(),
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
    theme_data = ThemeStub().model_dump()
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


def test_theme_read(logged_in_king):
    """test successful read of all themes"""
    # make a request to read
    client, king = logged_in_king
    theme_data = ThemeStub().model_dump()
    create_response = client.post("/api/theme/", json=theme_data)

    theme_id = next(iter(create_response.json["theme"].keys()))

    read_response = client.get(f"/api/theme/{theme_id}")
    assert read_response.status_code == http.OK
    assert create_response.json == read_response.json


######################################################################
# update
######################################################################


def test_theme_update_all_fields(logged_in_king):
    """test successful theme update with all fields."""
    client, king = logged_in_king
    original_data = ThemeStub().model_dump()

    create_response = client.post("/api/theme/", json=original_data)
    state = create_response.json
    theme_slice = state["theme"]
    theme_id = next(iter(theme_slice.keys()))
    theme = theme_slice[str(theme_id)]

    updated_data = ThemeStub().model_dump()
    updated_response = client.put(
        f"/api/theme/{theme_id}", json=updated_data
    )
    updated_state = updated_response.json
    updated_theme_slice = updated_state["theme"]
    updated_theme_id = next(iter(updated_theme_slice.keys()))
    updated_theme = updated_theme_slice[str(updated_theme_id)]

    # make sure unchangeable fields did not change
    assert updated_theme["id"] == theme["id"]
    assert updated_theme["created"] == theme["created"]
    assert updated_theme["king_id"] == theme["king_id"]

    # make sure changed fields have new values
    assert updated_theme["name"] == updated_data["name"]
    assert (
        updated_theme["background_color"]
        == updated_data["background_color"]
    )
    assert updated_theme["text_color"] == updated_data["text_color"]

    assert theme["updated"] < updated_theme["updated"]


######################################################################
# delete
######################################################################


def test_theme_delete_removes_from_db(logged_in_king, test_db):
    """test that theme deletion really deletes record from database."""
    import app

    app.debug = True

    client, king_data = logged_in_king
    theme_data = ThemeStub().model_dump()

    create_response = client.post("/api/theme/", json=theme_data)
    state = create_response.json
    theme_slice = state["theme"]
    theme_id = next(iter(theme_slice.keys()))
    # create_theme = theme_slice[str(theme_id)]

    # check the db to see if table "theme" has the record
    db_theme = test_db.session.get(Theme, theme_id)
    assert db_theme

    delete_response = client.delete(f"/api/theme/{theme_id}")
    delete_state = delete_response.json
    delete_theme_slice = delete_state["theme"]
    delete_theme_id = next(iter(delete_theme_slice.keys()))
    delete_theme = delete_theme_slice[str(delete_theme_id)]

    assert delete_theme is None
    assert delete_theme_id == theme_id

    deleted_theme = test_db.session.get(Theme, theme_id)
    assert deleted_theme is None
