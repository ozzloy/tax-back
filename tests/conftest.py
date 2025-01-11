"""configure tests."""

from flask.testing import FlaskClient
import pytest

from app import create_app
from app.db import db
from app.seed import seed
from config import Config


class TestConfig(Config):
    """test configuration."""

    TESTING = True
    CHECK_EMAIL_DELIVERABILITY = False


class CSRFTestClient(FlaskClient):
    """implicitly add csrf token to all non-get requests."""

    def __init__(self, *args, **kwargs):
        """Create a csrf client."""
        super().__init__(*args, **kwargs)
        self._csrf_token = None

    @property
    def csrf_token(self):
        """Return valid csrf token, requesting it if necessary."""
        if not self._csrf_token:
            response = super().get("/api/csrf-token")
            if response.status_code != 200:
                raise ValueError(
                    f"failed to get CSRF token: {response.status_code}"
                )
            if "csrf_token" not in response.json:
                raise ValueError("no CSRF token in response")
            self._csrf_token = response.json["csrf_token"]
        return self._csrf_token

    def _prepare_request(self, kwargs):
        """Add csrf and set content type for all requests."""
        kwargs.setdefault("headers", {})
        kwargs["content_type"] = "application/json"
        kwargs["headers"].setdefault("X-CSRF-TOKEN", self.csrf_token)
        return kwargs

    def post(self, *args, **kwargs):
        """Add csrf, set content type to application/json to posts."""
        return super().post(*args, **self._prepare_request(kwargs))

    def put(self, *args, **kwargs):
        """Add csrf, set content type to application/json to puts."""
        return super().put(*args, **self._prepare_request(kwargs))

    def patch(self, *args, **kwargs):
        """Add csrf, set content type to application/json to patches."""
        return super().patch(*args, **self._prepare_request(kwargs))

    def delete(self, *args, **kwargs):
        """Add csrf, set content type to application/json to deletes."""
        return super().delete(*args, **self._prepare_request(kwargs))


@pytest.fixture
def app():
    """Generate testing version of app."""
    app = create_app(TestConfig)
    app.test_client_class = CSRFTestClient

    with app.app_context():
        db.create_all()
        seed()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Get test client."""
    return app.test_client()
