import pytest
from bootstrap.config import AppConfig, CeleryConfig, EventConfig


@pytest.fixture(autouse=True)
def anyio_backend():
    """
    For now, we don't have reason to test anything but asyncio
    https://anyio.readthedocs.io/en/stable/testing.html
    """
    return "asyncio"


@pytest.fixture(scope="function")
def test_config() -> AppConfig:
    return AppConfig(
        SQLALCHEMY_CONFIG={},
        ENVIRONMENT="test",
        EVENTS=EventConfig(REDIS_BROKER_URL=""),
        CELERY=CeleryConfig(
            broker_url="",
            result_backend="",
        ),
    )
