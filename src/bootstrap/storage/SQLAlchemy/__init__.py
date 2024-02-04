from typing import Callable, Dict

from dependency_injector.wiring import Provide, inject
from sqlalchemy_bind_manager import SQLAlchemyBindManager

from . import default_bind_tables

TABLE_INIT_REGISTRY: Dict[str, Callable] = {
    "default": default_bind_tables.init_tables,
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
            init_function(bind.registry_mapper)
