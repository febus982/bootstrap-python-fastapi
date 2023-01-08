import os
from uuid import uuid4

import pytest
from dependency_injector.providers import Object
from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyBindConfig

from config import AppConfig
from di_container import Container
from storage import init_storage


@pytest.fixture(scope="function")
def testapp() -> Container:
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

    di_container = Container(  # type: ignore
        config=Object(test_config),
    )
    init_storage()
    sa_manager = di_container.SQLAlchemyBindManager()
    for k, v in sa_manager.get_binds().items():
        v.registry_mapper.metadata.create_all(v.engine)

    yield di_container
    os.unlink(test_db_path)
    clear_mappers()


@pytest.fixture
def anyio_backend():
    """
    For now, we don't have reason to test anything but asyncio
    https://anyio.readthedocs.io/en/stable/testing.html
    """
    return "asyncio"
