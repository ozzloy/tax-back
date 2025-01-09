"""test king routes"""


def test_king_read_all(client):
    """test king read all"""
    response = client.get("/api/king/")
    print(f"{response = }")
    print(f"{response.json = }")
    assert response.status_code == 200
