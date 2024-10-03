"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

from celery.signals import worker_process_init
from opentelemetry.instrumentation.celery import CeleryInstrumentor

from bootstrap import AppConfig, application_init


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    CeleryInstrumentor().instrument()  # pragma: nocover


app = application_init(AppConfig()).celery_app
