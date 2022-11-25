from typing import Callable

from dependency_injector.wiring import inject, Provide
from sqlalchemy_bind_manager import SQLAlchemyBindManager

from . import default_tables

TABLE_INIT_REGISTRY: dict[str, Callable] = {
    "default": default_tables.init_tables,
}


def init_sqlalchemy():
    init_tables()


@inject
def init_tables(
    sqlalchemy_manager: SQLAlchemyBindManager = Provide[SQLAlchemyBindManager.__name__],
):
    for name, bind in sqlalchemy_manager.get_binds().items():
        init_function = TABLE_INIT_REGISTRY.get(name)
        if init_function:
            init_function(bind)
