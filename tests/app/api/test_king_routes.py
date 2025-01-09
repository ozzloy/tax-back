from app.validator import king_validator


def test_king_create_success(client):
    response = client.post(
        "/api/king/",
        json={
            "nick": "bob",
            "email": "bob@example.com",
            "password": "i love laura",
        },
        content_type="application/json",
    )

    assert response.status_code == 201

    partial_state = response.json

    assert "king" in partial_state
    king_slice = partial_state["king"]
    king_validator.validate_king_slice(king_slice)


def test_king_read_all(client):
    response = client.get("/api/king/")
    assert response.status_code == 200
    state = response.json
    assert "king" in state
    king_slice = state["king"]
    for id_str, king in king_slice.items():
        assert id_str == str(king["id"])
        assert "nick" in king
