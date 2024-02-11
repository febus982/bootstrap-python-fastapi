from celery import Celery

from .config import AppConfig


def init_celery(config: AppConfig) -> Celery:
    celery_app = Celery(f"{config.APP_NAME}-celery")
    celery_app.config_from_object(config.CELERY)
    celery_app.autodiscover_tasks()

    return celery_app
