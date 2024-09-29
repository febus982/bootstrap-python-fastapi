from cloudevents_pydantic.events import CloudEvent
from structlog import get_logger


class NullEventGateway:
    async def emit(
        self, event: CloudEvent
    ) -> None:  # pragma: no cover # No need to test this
        logger = get_logger()
        await logger.ainfo(
            "Event emitted",
            cloudevent=event.model_dump(),
        )
