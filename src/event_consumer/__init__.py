"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

import os
from typing import Optional, Union

import structlog
from faststream import FastStream
from faststream.redis import RedisBroker, RedisRouter
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from common import AppConfig, application_init
from conftest import test_config
from domains import event_registry
from domains.books.events import BookCreatedV1, BookCreatedV1Data

"""
For the sake of this example app we reuse the domain registry,
which is used for publishing. In a real world these registries
are different and separate.
"""
subscriber_registry = event_registry


def setup_telemetry(service_name: str, otlp_endpoint: str) -> TracerProvider:
    resource = Resource.create(attributes={"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    return tracer_provider


def create_app(test_config: Union[AppConfig, None] = None) -> FastStream:
    config = test_config or AppConfig()
    setup_telemetry(
        "faststream", otlp_endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]
    )
    broker = application_init(config).faststream_broker
    register_subscribers(broker)
    if config.EVENTS.REGISTER_SUBSCRIBERS:
        register_subscribers(broker)

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


# TODO: Add Routing structure similar to the one in the fastapi implementation
def register_subscribers(broker: RedisBroker, topic: Optional[str] = None):
    if topic is not None and topic in subscriber_registry.keys():
        topics_map = {topic: subscriber_registry[topic]}
    else:
        topics_map = subscriber_registry.copy()

    logger = structlog.get_logger()
    router = RedisRouter()

    for topic, event_type in topics_map.items():

        @router.subscriber(topic)
        async def handler(msg: event_type) -> None:  # type: ignore[valid-type]
            logger.info(f"Received message {type(msg)} {msg}")

    broker.include_router(router)
