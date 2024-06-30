import os
from unittest import mock
from unittest.mock import patch

from bootstrap.config import AppConfig, CeleryConfig, EventConfig
from http_app import create_app

"""
We want to run tests without setting local environment variables.
All tests use test_config from the fixture but I want to test
the debug setting so we mock the env variables for this test only.
"""


@mock.patch.dict(
    os.environ,
    {
        "OTEL_SERVICE_NAME": "bootstrap-fastapi-worker",
        "OTEL_EXPORTER_OTLP_ENDPOINT": "http://otel-collector:4317",
        "CELERY__broker_url": "redis://redis:6379/0",
        "CELERY__result_backend": "redis://redis:6379/1",
        "EVENTS__REDIS_BROKER_URL": "redis://redis-events:6379",
    },
    clear=True,
)
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
