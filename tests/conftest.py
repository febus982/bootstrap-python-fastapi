import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app


@pytest.fixture
def anyio_backend():
    """
    For now, we don't have reason to test anything but asyncio
    https://anyio.readthedocs.io/en/stable/testing.html
    """
    return 'asyncio'


@pytest.fixture
def app() -> FastAPI:
    test_config = {
        "TESTING": True,
    }
    yield create_app(test_config=test_config)
