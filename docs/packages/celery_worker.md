# Celery worker

The `celery_worker` package is a small entrypoint to run Celery workers and beat.

The `Celery` class has to be initialised to invoke tasks from domain logic,
in addition to the worker, therefore we initialise it together with the generic
application init.

Celery tasks will be defined using the `shared_task` decorator, so we don't 
need to import the specific `Celery` class instance, as per Clean Architecture
principles.
