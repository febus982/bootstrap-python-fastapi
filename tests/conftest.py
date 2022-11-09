import pytest
from fastapi import FastAPI
from dependency_injector import providers
from sqlalchemy.orm import clear_mappers

from app import create_app, Container, AppConfig
from app.deps.sqlalchemy_manager import SQLAlchemyBindConfig


@pytest.fixture(scope="function")
def anyio_backend():
    """
    For now, we don't have reason to test anything but asyncio
    https://anyio.readthedocs.io/en/stable/testing.html
    """
    return 'asyncio'


@pytest.fixture(scope="function")
def app() -> FastAPI:
    test_config = AppConfig(
        SQLALCHEMY_CONFIG={
            "default": SQLAlchemyBindConfig(
                engine_url="sqlite:///./test.db",
                engine_options=dict(connect_args={"check_same_thread": False}),
            ),
        }
    )
    # TODO: better test config management (perhaps remove from DI container)
    c = Container()
    c.config.override(providers.Object(test_config))
    yield create_app(di_enabled=False)
    clear_mappers()
