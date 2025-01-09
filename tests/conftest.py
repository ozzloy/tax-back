import pytest

from app import create_app, db
from app.model import King
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        king = King(nick="bob")
        db.session.add(king)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_king_get_all(client):
    response = client.get("/api/king/")
    assert response.status_code == 200
    state = response.json
    assert "king" in state
    king_slice = state["king"]
    for king in king_slice.values():
        assert "nick" in king
