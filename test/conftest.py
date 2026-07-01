import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key",
    })
    return app


@pytest.fixture(scope="function")
def session(app):
    """Create fresh tables for each test, drop after."""
    with app.app_context():
        _db.create_all()
        yield _db.session
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, session):
    """Flask test client with fresh DB per test."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Flask test CLI runner."""
    return app.test_cli_runner()
