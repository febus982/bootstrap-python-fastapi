import logging
from typing import List

import structlog
from opentelemetry import trace
from structlog.typing import EventDict, Processor

from ..config import AppConfig
from .processors import (
    add_logging_open_telemetry_spans,
    drop_color_message_key,
    extract_from_record,
)


def init_logger(config: AppConfig) -> None:
    """
    Configure structlog and stdlib logging with shared handler and formatter.

    :param config: The app configuration
    :type config: AppConfig
    :return:
    """
    # Strongly inspired by https://gist.github.com/nymous/f138c7f06062b7c43c060bf03759c29e

    # These processors will be used by both structlog and stdlib logger
    shared_processors: List[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        drop_color_message_key,
        add_logging_open_telemetry_spans,
        structlog.processors.StackInfoRenderer(),
    ]

    # stdlib_processors are executed before the shared ones, so processors
    # accessing processor metadata such as `_extract_from_record` must
    # run here, before `remove_processors_meta`
    stdlib_processors: List[Processor] = [
        extract_from_record,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]

    log_level = logging.DEBUG if config.DEBUG else logging.INFO
    if config.ENVIRONMENT in ["local", "test"]:
        shared_processors.append(
            structlog.processors.TimeStamper(fmt="%d-%m-%Y %H:%M:%S", utc=True)
        )
        stdlib_processors.append(structlog.dev.ConsoleRenderer())
    else:
        shared_processors.append(structlog.processors.TimeStamper(fmt="iso", utc=True))
        shared_processors.append(structlog.processors.dict_tracebacks)
        stdlib_processors.append(structlog.processors.JSONRenderer())

    """
    Even if we set the loglevel using the stdlib setLevel later,
    using make_filtering_bound_logger will filter events before
    in the chain, producing a performance improvement
    """
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=[
            *shared_processors,
            # This prepares the log events to be handled by stdlib
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Create a handler for stdlib logger
    stdlib_handler = logging.StreamHandler()
    stdlib_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,
            processors=stdlib_processors,
        )
    )

    # Use structlog to format logs coming from stdlib logger
    stdlib_logger = logging.getLogger()
    # stdlib_logger.handlers.clear()
    stdlib_logger.addHandler(stdlib_handler)
    stdlib_logger.setLevel(log_level)

    for _log in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog. Initial messages from reloader startup are not caught.
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True
