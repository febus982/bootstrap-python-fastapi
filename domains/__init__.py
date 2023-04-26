from dependency_injector.providers import Object

from config import AppConfig
from di_container import Container


def init_domains(config: AppConfig):
    Container(
        config=Object(config),
    )
