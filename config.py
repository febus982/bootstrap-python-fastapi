import logging
import os
from typing import Dict, Literal, List

import structlog
from pydantic import BaseSettings
from sqlalchemy_bind_manager import SQLAlchemyBindConfig
from structlog.typing import Processor

TYPE_ENVIRONMENT = Literal['local', 'test', 'staging', 'production']


class AppConfig(BaseSettings):
    SQLALCHEMY_CONFIG: Dict[str, SQLAlchemyBindConfig] = {
        "default": SQLAlchemyBindConfig(
            engine_url=f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/sqlite.db",
            engine_options=dict(connect_args={"check_same_thread": False}, echo=True),
            session_options=dict(expire_on_commit=False),
        ),
        # Add additional bindings here, e.g.:
        # "customer": SQLAlchemyBindConfig(engine_url="sqlite:///./customer.db"),
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

