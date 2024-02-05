from collections.abc import AsyncIterator

import pytest
from bootstrap.storage.SQLAlchemy import init_tables
from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyAsyncConfig, SQLAlchemyBindManager


@pytest.fixture(scope="function")
async def test_sa_manager() -> AsyncIterator[SQLAlchemyBindManager]:
    clear_mappers()

    db_config = SQLAlchemyAsyncConfig(
        engine_url="sqlite+aiosqlite://",
        engine_options=dict(connect_args={"check_same_thread": False}),
    )
    sa_manager = SQLAlchemyBindManager(config=db_config)
    init_tables(sqlalchemy_manager=sa_manager)
    for k, v in sa_manager.get_binds().items():
        async with v.engine.begin() as conn:  # type: ignore
            await conn.run_sync(v.registry_mapper.metadata.create_all)

    yield sa_manager
    clear_mappers()
