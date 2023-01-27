import logging
import os
from typing import Literal, List

import structlog
from pydantic import BaseSettings
from sqlalchemy_bind_manager import SQLAlchemyAsyncBindConfig, SQLAlchemyBindConfig
from structlog.typing import Processor

TYPE_ENVIRONMENT = Literal["local", "test", "staging", "production"]


class AppConfig(BaseSettings):
    SQLALCHEMY_CONFIG = {
        "default": SQLAlchemyAsyncBindConfig(
            engine_url=f"sqlite+aiosqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db",
            engine_options=dict(
                connect_args={
                    "check_same_thread": False,
                },
                echo=True,
                future=True,
            ),
        ),
    }
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"


class AlembicConfig(BaseSettings):
    """
    It's extremely complex coordinating transaction on multiple binds
    when using Async engines. For the moment we stick using a custom config
    with sync engines, waiting to get a better Alembic implementation.
    E.g.
    https://github.com/testdrivenio/fastapi-sqlmodel-alembic/blob/main/project/migrations/env.py
    """

    SQLALCHEMY_CONFIG = {
        "default": SQLAlchemyBindConfig(
            engine_url=f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db",
            engine_options=dict(
                connect_args={"check_same_thread": False}, echo=True, future=True
            ),
        ),
    }
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"


def init_logger(config: AppConfig):

    processors: List[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
    ]

    if config.ENVIRONMENT not in ["local", "test"]:
        log_level = logging.INFO
        processors.append(structlog.processors.dict_tracebacks)
        processors.append(structlog.processors.JSONRenderer())
    else:
        log_level = logging.DEBUG
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.stdlib.recreate_defaults()
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
