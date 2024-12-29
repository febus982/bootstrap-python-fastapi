from common import AppConfig
from http_app import context
from http_app.dependencies import app_config


def test_app_config_return_context_variable():
    config = AppConfig(APP_NAME="SomeOtherAppName")
    context.app_config.set(config)
    assert app_config() is config
