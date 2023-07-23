from cloudevents.pydantic import CloudEvent
from structlog import get_logger


class NullEventGateway:
    async def emit(self, event: CloudEvent) -> None:
        logger = get_logger()
        await logger.ainfo("Event emitted", cloudevent=event.dict())
