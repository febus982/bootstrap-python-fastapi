import os
from uuid import uuid4

import pytest
from fastapi import FastAPI
from dependency_injector import providers
from sqlalchemy.orm import clear_mappers

from app import create_app, Container, AppConfig
from app.deps.sqlalchemy_manager import SQLAlchemyBindConfig, SQLAlchemyManager


@pytest.fixture(scope="function")
def anyio_backend():
    """
    For now, we don't have reason to test anything but asyncio
    https://anyio.readthedocs.io/en/stable/testing.html
    """
    return 'asyncio'


@pytest.fixture(scope="function")
def app() -> FastAPI:
    test_db_path = f"./{uuid4()}.db"
    test_config = AppConfig(
        SQLALCHEMY_CONFIG={
            "default": SQLAlchemyBindConfig(
                engine_url=f"sqlite:///{test_db_path}",
                engine_options=dict(connect_args={"check_same_thread": False}),
            ),
        }
    )
    # TODO: better test config management (perhaps remove from DI container)
    c = Container()
    c.config.override(providers.Object(test_config))

    sa_manager: SQLAlchemyManager = c.SQLAlchemyManager()
    for k, v in sa_manager.get_binds().items():
        v.registry_mapper.metadata.create_all(v.engine)

    yield create_app(di_enabled=False)
    clear_mappers()
    os.unlink(test_db_path)
