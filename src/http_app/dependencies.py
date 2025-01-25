from common import AppConfig
from http_app import context


def app_config() -> AppConfig:
    return context.app_config.get()
