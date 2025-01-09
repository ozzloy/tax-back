from flask.testing import FlaskClient
import pytest

from app import create_app, db
from app.model import King
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    CHECK_EMAIL_DELIVERABILITY = False


class CSRFTestClient(FlaskClient):
    """implicitly add csrf token to all non-get requests"""

    def __init__(self, *args, **kwargs):
        """create a csrf client"""
        super().__init__(*args, **kwargs)
        self._csrf_token = None

    @property
    def csrf_token(self):
        """return valid csrf token, requesting it if necessary"""
        if not self._csrf_token:
            response = super().get("/api/csrf-token")
            self._csrf_token = response.json["csrf_token"]
        return self._csrf_token

    def _prepare_request(self, kwargs):
        """add csrf and set content type for all requests"""
        kwargs.setdefault("headers", {})
        kwargs["content_type"] = "application/json"
        kwargs["headers"].setdefault("X-CSRF-TOKEN", self.csrf_token)
        return kwargs

    def post(self, *args, **kwargs):
        return super().post(*args, **self._prepare_request(kwargs))

    def put(self, *args, **kwargs):
        return super().put(*args, **self._prepare_request(kwargs))

    def patch(self, *args, **kwargs):
        return super().patch(*args, **self._prepare_request(kwargs))

    def delete(self, *args, **kwargs):
        return super().delete(*args, **self._prepare_request(kwargs))


@pytest.fixture
def app():
    """generate testing version of app"""
    app = create_app(TestConfig)
    app.test_client_class = CSRFTestClient

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """get test client"""
    return app.test_client()
