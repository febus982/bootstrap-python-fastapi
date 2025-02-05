from common import AppConfig
from http_app import context
from http_app.dependencies import get_app_config


def test_app_config_return_context_variable():
    config = AppConfig(APP_NAME="SomeOtherAppName")
    context.app_config.set(config)
    assert get_app_config() is config
