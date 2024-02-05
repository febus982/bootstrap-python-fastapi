from unittest.mock import patch

from bootstrap.config import AppConfig
from http_app import create_app


def test_with_default_config() -> None:
    """Test create_app without passing test config."""
    with patch("bootstrap.bootstrap.init_storage", return_value=None):
        app = create_app()
    assert app.debug is False


def test_with_debug_config() -> None:
    # We don't need the storage to test the HTTP app
    with patch("bootstrap.bootstrap.init_storage", return_value=None):
        app = create_app(
            test_config=AppConfig(
                SQLALCHEMY_CONFIG={},
                ENVIRONMENT="test",
                DEBUG=True,
            )
        )

    assert app.debug is True
