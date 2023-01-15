import os
from uuid import uuid4

import pytest
from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyBindConfig

from config import AppConfig
from http_app import create_app


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
        },
        ENVIRONMENT="test",
    )

    app = create_app(test_config=test_config)
    sa_manager = app.di_container.SQLAlchemyBindManager()
    for k, v in sa_manager.get_binds().items():
        v.registry_mapper.metadata.create_all(v.engine)

    yield app
    os.unlink(test_db_path)
    clear_mappers()
