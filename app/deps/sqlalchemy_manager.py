from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, registry, Session, declarative_base

from app.deps.singleton import Singleton


class SQLAlchemyBindConfig(BaseModel):
    engine_url: str
    engine_options: dict = dict()
    session_options: dict = dict()


@dataclass
class SQLAlchemyBind:
    engine: Engine
    registry_mapper: registry
    session_class: sessionmaker
    model_declarative_base: Any


SQLAlchemyConfig = TypeVar('SQLAlchemyConfig', bound=dict[str, SQLAlchemyBindConfig] | SQLAlchemyBindConfig)


class SQLAlchemyManager(metaclass=Singleton):
    __binds: dict[str, SQLAlchemyBind] = {}

    def init(self, config: SQLAlchemyConfig) -> None:
        if isinstance(config, SQLAlchemyBindConfig):
            self.__init_bind("default", config)

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
            raise ValueError("Config has to be a SQLAlchemyBindConfig object")

        engine_options = dict(
            echo=True,
            future=True,
        )
        engine_options.update(config.engine_options)

        session_options = dict(
            autocommit=False,
            autoflush=False,
            # expire_on_commit=False,
        )
        session_options.update(config.session_options)

        engine = create_engine(config.engine_url, **engine_options)
        registry_mapper = registry()
        self.__binds[name] = SQLAlchemyBind(
            engine=engine,
            registry_mapper=registry_mapper,
            session_class=sessionmaker(bind=engine, **session_options),
            model_declarative_base=declarative_base(metadata=registry_mapper.metadata)
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
