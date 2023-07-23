from typing import Protocol

from cloudevents.pydantic import CloudEvent
from structlog import get_logger


class EventGatewayInterface(Protocol):
    async def emit(self, event: CloudEvent) -> None:
        pass


class NullEventGateway:
    async def emit(self, event: CloudEvent) -> None:
        logger = get_logger()
        await logger.ainfo("Event emitted", cloudevent=event.dict())
