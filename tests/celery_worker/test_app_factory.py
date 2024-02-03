from celery import Celery
from celery_worker import app


def test_factory():
    # Hopefully this is enough to be sure we can run
    # `celery -A celery_worker.app worker`
    assert isinstance(app, Celery)
    assert app.configured
