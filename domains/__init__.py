from dependency_injector.providers import Object

from config import AppConfig, init_logger
from di_container import Container


def init_domains(config: AppConfig):
    init_logger(config)
    Container(
        config=Object(config),
    )
