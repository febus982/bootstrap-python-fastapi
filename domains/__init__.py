from celery import Celery
from dependency_injector.providers import Object

from config import AppConfig
from di_container import Container


def init_domains(config: AppConfig):
    Container(
        config=Object(config),
    )


def init_celery(config: AppConfig) -> Celery:
    celery_app = Celery()
    celery_app.config_from_object(config.CELERY)
    celery_app.autodiscover_tasks()

    return celery_app
