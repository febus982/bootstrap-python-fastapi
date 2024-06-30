"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones).

The only operation is assigning the already initalised Celery
to a global variable because  Celery CLI can't run using a factory
function.

No need for testing.
"""
# pragma: no cover

from bootstrap import AppConfig, application_init

app = application_init(AppConfig()).celery_app
