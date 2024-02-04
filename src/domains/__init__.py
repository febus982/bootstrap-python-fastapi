from bootstrap.config import AppConfig
from bootstrap.di_container import Container
from celery import Celery
from dependency_injector.providers import Object


def init_domains(config: AppConfig):
    Container(
        config=Object(config),
    )


def init_celery(config: AppConfig) -> Celery:
    celery_app = Celery(f"{config.APP_NAME}-celery")
    celery_app.config_from_object(config.CELERY)
    celery_app.autodiscover_tasks()

    return celery_app
