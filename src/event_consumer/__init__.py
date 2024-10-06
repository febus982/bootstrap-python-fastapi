"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""
import os
from typing import Annotated, Union, Dict, Type, Optional, List

import structlog
from pydantic import Field

from bootstrap import AppConfig, application_init
from faststream import FastStream, Logger
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from domains.books.events import BookCreatedV1, BookUpdatedV1, BookCreatedV1Data

_event_registry: Dict[str, Type] = {
    'books': Annotated[
        Union[BookCreatedV1, BookUpdatedV1], Field(discriminator="type")
    ]
}

def setup_telemetry(service_name: str, otlp_endpoint: str) -> TracerProvider:
    resource = Resource.create(attributes={"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    return tracer_provider


def register_subscribers(broker, topics: Optional[List[str]] = None):
    if topics is None:
        topics_map: Dict[str, Type] = _event_registry
    else:
        topics_map: Dict[str, Type] = {k: v for k, v in _event_registry.items() if k in topics}


    for topic, event_type in topics_map.items():
        @broker.subscriber(topic)  # type: ignore
        async def handler(msg: event_type, logger: Logger) -> None:
            logger.info(f"Received message {type(msg)} {msg}")
            # logger.info(f"Received message {type(msg)} {msg}", extra={"msg": "some_extra_here"})
            # l = logging.getLogger()
            # l.info("AAAAA", extra={"eee": "AAA"})


def create_app(
    test_config: Union[AppConfig, None] = None
) -> FastStream:
    setup_telemetry("faststream", otlp_endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"])
    broker = application_init(AppConfig()).faststream_broker
    app = FastStream(broker, logger=structlog.get_logger())
    register_subscribers(broker)

    publisher = broker.publisher("books", schema=_event_registry["books"])

    @app.after_startup
    async def after_startup():
        await broker.publish(BookCreatedV1.event_factory(
            data=BookCreatedV1Data(
                book_id=123,
                title="AAA",
                author_name="BBB",
            )
        ), "books")


    return app
