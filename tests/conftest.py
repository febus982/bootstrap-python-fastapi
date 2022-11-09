import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import clear_mappers

from app import create_app, AppConfig
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
    # test_config = AppConfig(
    #     SQLALCHEMY_CONFIG={
    #         "default": SQLAlchemyBindConfig(
    #             engine_url="sqlite:///./test.db",
    #             engine_options=dict(connect_args={"check_same_thread": False}),
    #         ),
    #     }
    # )
    yield create_app(test_config={"TEST":True})
    clear_mappers()
