from contextvars import ContextVar

from common import AppConfig

app_config: ContextVar[AppConfig] = ContextVar("app_config")
