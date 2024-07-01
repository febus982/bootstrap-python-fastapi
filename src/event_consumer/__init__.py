"""
This is a tiny layer that takes care  of initialising the shared
application layers (storage, logs) when running standalone workers
without having to initialise the HTTP framework (or other ones)
"""

import os

import structlog
from bootstrap import AppConfig, application_init
from domains.events import BookCreatedV1
from faststream import FastStream, Logger
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_telemetry(service_name: str, otlp_endpoint: str) -> TracerProvider:
    resource = Resource.create(attributes={"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    return tracer_provider


broker = application_init(AppConfig()).faststream_broker
setup_telemetry("faststream", otlp_endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"])
app = FastStream(broker, logger=structlog.get_logger())


@broker.subscriber("books_topic")  # type: ignore
async def handle_msg(msg: BookCreatedV1, logger: Logger) -> None:
    logger.info("Received message", extra={"msg": "some_extra_here"})
    # l = logging.getLogger()
    # l.info("AAAAA", extra={"eee": "AAA"})
