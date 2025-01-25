from typing import cast

from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Object

# from gateways.event import FastStreamRedisGateway
from pydantic import BaseModel, ConfigDict

from .config import AppConfig
from .di_container import Container
from .dramatiq import init_dramatiq
from .event_publisher import init_broker
from .logs import init_logger
from .storage import init_storage


class InitReference(BaseModel):
    di_container: DynamicContainer

    model_config = ConfigDict(arbitrary_types_allowed=True)


def application_init(app_config: AppConfig) -> InitReference:
    container = cast(
        DynamicContainer,  # Make mypy happy
        Container(
            config=Object(app_config),
        ),
    )
    init_logger(app_config)
    init_storage()
    init_dramatiq(app_config)
    router = init_broker(app_config.EVENTS)
    # This is temporary, has to go directly in the Container
    # container.BookEventGatewayInterface.override(
    #     Object(FastStreamRedisGateway(broker=broker))
    # )

    return InitReference(
        di_container=container,
        faststream_broker=router,
    )
