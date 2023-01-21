import os
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
from grpc import Server
from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyBindConfig

from config import AppConfig
from grpc_app import create_server


@pytest.fixture(scope="function")
async def testserver() -> AsyncIterator[Server]:
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

    server = create_server(test_config=test_config)
    sa_manager = server.container.SQLAlchemyBindManager()
    for k, v in sa_manager.get_binds().items():
        v.registry_mapper.metadata.create_all(v.engine)

    server.start()
    yield server
    server.stop(grace=0)
    os.unlink(test_db_path)
    clear_mappers()
