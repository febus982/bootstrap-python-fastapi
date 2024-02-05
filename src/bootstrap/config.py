from pathlib import Path
from typing import Dict, Literal, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy_bind_manager import SQLAlchemyAsyncConfig

TYPE_ENVIRONMENT = Literal["local", "test", "staging", "production"]


class CeleryConfig(BaseModel):
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#configuration

    timezone: str = "UTC"

    # Broker config
    broker_url: Optional[str] = None
    broker_connection_retry_on_startup: bool = True

    # Results backend config
    result_backend: Optional[str] = None
    redis_socket_keepalive: bool = True

    # Enable to ignore the results by default and not produce tombstones
    task_ignore_result: bool = False

    # We want to use the default python logger configured using structlog
    worker_hijack_root_logger: bool = False

    # Events enabled for monitoring
    worker_send_task_events: bool = True
    task_send_sent_event: bool = True

    # Recurring tasks triggered directly by Celery
    beat_schedule: dict = {}
    # beat_schedule: dict = {
    #     "recurrent_example": {
    #         "task": "domains.books._tasks.book_cpu_intensive_task",
    #         "schedule": 5.0,
    #         "args": ("a-random-book-id",),
    #     },
    # }


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    APP_NAME: str = "bootstrap"
    CELERY: CeleryConfig = CeleryConfig()
    DEBUG: bool = False
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"
    SQLALCHEMY_CONFIG: Dict[str, SQLAlchemyAsyncConfig] = dict(
        default=SQLAlchemyAsyncConfig(
            engine_url=f"sqlite+aiosqlite:///{Path(__file__).parent.parent.joinpath('sqlite.db')}",
            engine_options=dict(
                connect_args={
                    "check_same_thread": False,
                },
                echo=False,
                future=True,
            ),
        ),
    )
