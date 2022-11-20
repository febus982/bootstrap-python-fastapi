from typing import Callable

from dependency_injector.wiring import inject, Provide

from deps.sqlalchemy_manager import SQLAlchemyManager

from . import default_tables

TABLE_INIT_REGISTRY: dict[str, Callable] = {
    "default": default_tables.init_tables,
}


def init_sqlalchemy():
    init_tables()


@inject
def init_tables(
    sqlalchemy_manager: SQLAlchemyManager = Provide[SQLAlchemyManager.__name__],
):
    for name, bind in sqlalchemy_manager.get_binds().items():
        init_function = TABLE_INIT_REGISTRY.get(name)
        if init_function:
            init_function(bind)
