from dependency_injector.wiring import inject, Provide

from deps.sqlalchemy_manager import SQLAlchemyManager

from . import default_tables


def init_sqlalchemy():
    init_tables()


@inject
def init_tables(sqlalchemy_manager: SQLAlchemyManager = Provide[SQLAlchemyManager.__name__]):
    function_registry: dict[str, callable] = {
        "default": default_tables.init_tables,
    }
    for name, bind in sqlalchemy_manager.get_binds().items():
        init_function = function_registry.get(name)
        if init_function:
            init_function(bind)
