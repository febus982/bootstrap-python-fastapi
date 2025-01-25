"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

import os
from typing import Union, Optional

import structlog
from faststream import FastStream
from faststream.redis import RedisRouter
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from alembic.env import logger
from common import AppConfig, application_init
from domains import event_registry
from domains.books.events import BookCreatedV1, BookCreatedV1Data


def setup_telemetry(service_name: str, otlp_endpoint: str) -> TracerProvider:
    resource = Resource.create(attributes={"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    return tracer_provider


def create_app(test_config: Union[AppConfig, None] = None) -> FastStream:
    setup_telemetry(
        "faststream", otlp_endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]
    )
    router = application_init(AppConfig()).faststream_broker
    broker = router.broker
    app = FastStream(broker, logger=structlog.get_logger())

    @app.after_startup
    async def after_startup():
        await broker.publish(
            BookCreatedV1.event_factory(
                data=BookCreatedV1Data(
                    book_id=123,
                    title="AAA",
                    author_name="BBB",
                )
            ),
            "books",
        )

    return app



# TODO: Add Routing structure similar to the one in the fastapi and
#       move this in the event_consumer_module
def register_subscribers(router: RedisRouter, topic: Optional[str] = None):
    if topic is not None and topic in event_registry.keys():
        topics_map = {topic: event_registry[topic]}
    else:
        topics_map = event_registry.copy()

    logger = structlog.get_logger()

    for topic, event_type in topics_map.items():
        @router.subscriber(topic)
        async def handler(msg: event_type) -> None:  # type: ignore[valid-type]
            logger.info(f"Received message {type(msg)} {msg}")
