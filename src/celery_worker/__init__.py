"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

from bootstrap import AppConfig, application_init

app = application_init(AppConfig()).celery_app
