"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

import os
from typing import Union

import structlog
from faststream import FastStream
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from bootstrap import AppConfig, application_init
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
    broker = application_init(AppConfig()).faststream_broker
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
