import os
from collections.abc import Iterator
from uuid import uuid4

import pytest
from dependency_injector.providers import Object
from sqlalchemy.orm import clear_mappers

from di_container import Container
from storage import init_storage


@pytest.fixture(scope="function", autouse=True)
def test_di_container(test_config) -> Iterator[Container]:
    test_db_path = f"./{uuid4()}.db"
    clear_mappers()

    test_config.SQLALCHEMY_CONFIG["default"].engine_url = f"sqlite:///{test_db_path}"
    di_container = Container(
        config=Object(test_config),
    )
    init_storage()
    sa_manager = di_container.SQLAlchemyBindManager()
    for k, v in sa_manager.get_binds().items():
        # TODO: Review this typing on sqlalchemy_bind_manager (AsyncEngine not compatible with create_all
        v.registry_mapper.metadata.create_all(v.engine)  # type: ignore

    yield di_container
    os.unlink(test_db_path)
    clear_mappers()
