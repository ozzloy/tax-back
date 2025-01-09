"""test king routes"""


def test_king_read_all(client):
    response = client.get("/api/king/")
    assert response.status_code == 200
    state = response.json
    assert "king" in state
    king_slice = state["king"]
    for id_str, king in king_slice.items():
        assert id_str == str(king["id"])
        assert "nick" in king
