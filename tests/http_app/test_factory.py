from unittest.mock import patch

from bootstrap.config import AppConfig, EventConfig, CeleryConfig
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
                EVENTS=EventConfig(REDIS_BROKER_URL=""),
                CELERY=CeleryConfig(
                    broker_url="",
                    result_backend="",
                ),
            )
        )

    assert app.debug is True
