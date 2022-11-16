from contextlib import AbstractContextManager
from typing import TypeVar, ClassVar, NewType

from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, registry, Session


class SQLAlchemyBindConfig(BaseModel):
    engine_url: str
    engine_options: dict = dict()
    session_options: dict = dict()


class SQLAlchemyBind(BaseModel):
    engine: Engine
    registry_mapper: registry
    session_class: sessionmaker
    model_declarative_base: type

    class Config:
        arbitrary_types_allowed = True


# SQLAlchemyConfig = NewType("SQLAlchemyConfig", dict[str, SQLAlchemyBindConfig] | SQLAlchemyBindConfig)
SQLAlchemyConfig = TypeVar('SQLAlchemyConfig', bound=dict[str, SQLAlchemyBindConfig] | SQLAlchemyBindConfig)


class SQLAlchemyManager:
    __binds: dict[str, SQLAlchemyBind] = {}

    def __init__(self, config: SQLAlchemyConfig) -> None:
        if isinstance(config, SQLAlchemyBindConfig):
            self.__init_bind("default", config)

        if isinstance(config, dict):
            for name, conf in config.items():
                self.__init_bind(name, conf)

        # Shared session example
        # cls.__session_class = sessionmaker(
        #     binds={
        #         m: b.engine
        #         for b in cls.__binds.values()
        #         for m in b.registry_mapper.mappers
        #     },
        #     autocommit=False,
        #     autoflush=False,
        #     expire_on_commit=False,
        # )

    def __init_bind(self, name: str, config: SQLAlchemyBindConfig) -> None:
        if not isinstance(config, SQLAlchemyBindConfig):
            print(name, config)
            raise ValueError("Config has to be a SQLAlchemyBindConfig object")

        engine_options = dict(
            echo=False,
            future=True,
        )
        engine_options.update(config.engine_options)

        session_options = dict()
        session_options.update(config.session_options)

        engine = create_engine(config.engine_url, **engine_options)
        registry_mapper = registry()
        self.__binds[name] = SQLAlchemyBind(
            engine=engine,
            registry_mapper=registry_mapper,
            session_class=sessionmaker(bind=engine, **session_options),
            model_declarative_base=registry_mapper.generate_base()
        )

    def get_binds(self) -> dict[str, SQLAlchemyBind]:
        return self.__binds

    def get_bind_mappers_metadata(self) -> dict[str, MetaData]:
        """
        Returns the mappers metadata in a format that can be used
        in Alembic configuration

        :returns: mappers metadata
        :rtype: dict
        """
        return {k: b.registry_mapper.metadata for k, b in self.__binds.items()}

    def __get_bind(self, bind) -> SQLAlchemyBind:
        return self.__binds[bind]

    def get_session(self, bind: str = "default") -> AbstractContextManager[Session]:
        return self.__get_bind(bind).session_class()

    def get_mapper(self, bind: str = "default") -> registry:
        return self.__get_bind(bind).registry_mapper
