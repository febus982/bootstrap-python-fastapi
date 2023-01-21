from uuid import uuid4

import pytest
from dependency_injector.providers import Object
from sqlalchemy_bind_manager import SQLAlchemyAsyncBindConfig

from config import AppConfig
from di_container import Container


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
        SQLALCHEMY_CONFIG={
            "default": SQLAlchemyAsyncBindConfig(
                engine_url=f"sqlite+aiosqlite:///{uuid4()}.db",
                engine_options=dict(connect_args={"check_same_thread": False}),
            ),
        },
        ENVIRONMENT="test",
    )


@pytest.fixture(scope="function")
def test_container(test_config) -> Container:
    return Container(config=Object(test_config))
