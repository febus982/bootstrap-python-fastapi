import os
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
from dependency_injector.providers import Object
from sqlalchemy.orm import clear_mappers

from di_container import Container
from storage import init_storage


@pytest.fixture(scope="function", autouse=True)
async def test_di_container(test_config) -> AsyncIterator[Container]:
    test_db_path = f"./{uuid4()}.db"
    clear_mappers()

    test_config.SQLALCHEMY_CONFIG[
        "default"
    ].engine_url = f"sqlite+aiosqlite:///{test_db_path}"
    di_container = Container(
        config=Object(test_config),
    )
    init_storage()
    sa_manager = di_container.SQLAlchemyBindManager()
    for k, v in sa_manager.get_binds().items():
        async with v.engine.begin() as conn:  # type: ignore
            await conn.run_sync(v.registry_mapper.metadata.create_all)

    yield di_container
    try:
        os.unlink(test_db_path)
    except FileNotFoundError:
        pass
    clear_mappers()
