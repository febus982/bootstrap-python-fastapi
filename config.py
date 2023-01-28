import logging
import os
from typing import Literal, List

import structlog
from pydantic import BaseSettings
from sqlalchemy_bind_manager import SQLAlchemyAsyncBindConfig
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
                echo=False,
                future=True,
            ),
        ),
    }
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"


def init_logger(config: AppConfig):
    """
    Configure structlog and stdlib logging with shared handler and formatter.

    :param config: The app configuration
    :type config: AppConfig
    :return:
    """
    # These processors will be used by both structlog and stdlib logger
    processors: List[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
    ]

    if config.ENVIRONMENT not in ["local", "test"]:
        log_level = logging.INFO
        processors.append(structlog.stdlib.ProcessorFormatter.remove_processors_meta)
        processors.append(structlog.processors.TimeStamper(fmt="iso", utc=True))
        processors.append(structlog.processors.dict_tracebacks)
        processors.append(structlog.processors.JSONRenderer())
    else:
        log_level = logging.DEBUG
        processors.append(structlog.stdlib.ProcessorFormatter.remove_processors_meta)
        processors.append(structlog.processors.TimeStamper(fmt="%d-%m-%Y %H:%M:%S", utc=True))
        processors.append(structlog.dev.ConsoleRenderer(pad_event=30))

    structlog.stdlib.recreate_defaults()
    """
    Even if we set the loglevel using the stdlib setLevel later,
    using make_filtering_bound_logger will filter events before
    in the chain, producing a performance improvement
    """
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=[
            # This prepares the log events to be handled by stdlib
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    stdlib_handler = logging.StreamHandler()
    # Use structlog `ProcessorFormatter` to format all `logging` entries
    stdlib_handler.setFormatter(structlog.stdlib.ProcessorFormatter(
        processors=processors,
    ))
    stdlib_logger = logging.getLogger()
    stdlib_logger.addHandler(stdlib_handler)
    stdlib_logger.setLevel(log_level)

    for _log in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog. Initial messages from reloader startup are not caught.
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True
