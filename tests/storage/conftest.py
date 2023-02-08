import os
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyBindManager, SQLAlchemyAsyncConfig

from storage.SQLAlchemy import init_tables


@pytest.fixture(scope="function")
async def test_sa_manager() -> AsyncIterator[SQLAlchemyBindManager]:
    test_db_path = f"./{uuid4()}.db"
    clear_mappers()

    db_config = SQLAlchemyAsyncConfig(
        engine_url=f"sqlite+aiosqlite:///{test_db_path}",
        engine_options=dict(connect_args={"check_same_thread": False}),
    )
    sa_manager = SQLAlchemyBindManager(config=db_config)
    init_tables(sqlalchemy_manager=sa_manager)
    for k, v in sa_manager.get_binds().items():
        async with v.engine.begin() as conn:  # type: ignore
            await conn.run_sync(v.registry_mapper.metadata.create_all)

    yield sa_manager
    try:
        os.unlink(test_db_path)
    except FileNotFoundError:
        pass
    clear_mappers()
