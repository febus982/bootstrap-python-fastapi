from app.deps.sqlalchemy_manager import SQLAlchemyManager, SQLAlchemyConfig

from . import default_tables


def init_sqlalchemy(sqlalchemy_config: SQLAlchemyConfig):
    SQLAlchemyManager().init(sqlalchemy_config)
    init_tables()


def init_tables():
    function_registry: dict[str, callable] = {
        "default": default_tables.init_tables,
    }
    for name, bind in SQLAlchemyManager().get_binds().items():
        init_function = function_registry.get(name)
        if init_function:
            init_function(bind)
