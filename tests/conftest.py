import os
from uuid import uuid4

import pytest
from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from app import create_app, AppConfig
from deps.sqlalchemy_manager import SQLAlchemyBindConfig


@pytest.fixture(scope="function")
def testapp() -> FastAPI:
    test_db_path = f"./{uuid4()}.db"
    clear_mappers()
    test_config = AppConfig(
        SQLALCHEMY_CONFIG={
            "default": SQLAlchemyBindConfig(
                engine_url=f"sqlite:///{test_db_path}",
                engine_options=dict(connect_args={"check_same_thread": False}),
                session_options=dict(expire_on_commit=False),
            ),
        }
    )

    yield create_app(test_config=test_config)
    os.unlink(test_db_path)
    clear_mappers()

@pytest.fixture
def anyio_backend():
    """
    For now, we don't have reason to test anything but asyncio
    https://anyio.readthedocs.io/en/stable/testing.html
    """
    return 'asyncio'
