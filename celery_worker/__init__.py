"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""
from config import AppConfig, init_logger
from domains import init_celery, init_domains
from gateways.storage import init_storage

app_config = AppConfig()
init_logger(app_config)
init_domains(app_config)
init_storage()
app = init_celery(app_config)
