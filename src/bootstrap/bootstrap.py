from typing import Any

from celery import Celery
from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Object
from faststream.broker.core.usecase import BrokerUsecase
from pydantic import BaseModel, ConfigDict

from .celery import init_celery
from .config import AppConfig
from .di_container import Container
from .faststream import init_broker
from .logs import init_logger
from .storage import init_storage


class InitReference(BaseModel):
    celery_app: Celery
    di_container: DynamicContainer
    faststream_broker: BrokerUsecase[Any, Any]

    model_config = ConfigDict(arbitrary_types_allowed=True)


def application_init(app_config: AppConfig) -> InitReference:
    container = Container(
        config=Object(app_config),
    )
    init_logger(app_config)
    init_storage()
    celery = init_celery(app_config)
    broker = init_broker(app_config)

    return InitReference(
        celery_app=celery,
        di_container=container,
        faststream_broker=broker,
    )
