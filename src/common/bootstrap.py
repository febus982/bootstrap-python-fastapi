from dependency_injector.containers import Container as DI_Container
from dependency_injector.providers import Object
from pydantic import BaseModel, ConfigDict

from .asyncapi import init_asyncapi_info
from .config import AppConfig
from .di_container import Container
from .dramatiq import init_dramatiq
from .logs import init_logger
from .storage import init_storage
from .telemetry import instrument_opentelemetry


class InitReference(BaseModel):
    di_container: DI_Container

    model_config = ConfigDict(arbitrary_types_allowed=True)


def application_init(
    app_config: AppConfig,
    external_di_container: Container | None = None,
) -> InitReference:
    container = external_di_container or Container(
        config=Object(app_config),
    )
    init_logger(app_config)
    init_storage()
    init_dramatiq(app_config)
    init_asyncapi_info(app_config.APP_NAME)
    instrument_opentelemetry(app_config)

    return InitReference(
        di_container=container,
    )
