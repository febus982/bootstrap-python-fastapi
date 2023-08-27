from celery import Celery
from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Object
from pydantic import BaseModel, ConfigDict

from domains import init_celery, init_domains
from gateways.storage import init_storage

from .config import AppConfig, init_logger
from .di_container import Container


class InitReference(BaseModel):
    celery_app: Celery
    di_container: DynamicContainer

    model_config = ConfigDict(arbitrary_types_allowed=True)


def application_init(app_config: AppConfig) -> InitReference:
    container = Container(
        config=Object(app_config),
    )
    init_logger(app_config)
    init_domains(app_config)
    init_storage()
    celery = init_celery(app_config)

    return InitReference(
        celery_app=celery,
        di_container=container,
    )