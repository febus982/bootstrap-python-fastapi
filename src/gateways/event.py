import httpx
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


class HttpEventGateway:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def emit(
        self, event: CloudEvent
    ) -> None:
        logger = get_logger()
        await logger.ainfo(
            "Event emitted via HTTP request",
            cloudevent=event.model_dump(),
        )


# https://www.confluent.io/blog/kafka-python-asyncio-integration/
class KafkaEventGateway:
    pass