import asyncio
from functools import wraps

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk._configuration import _init_logging as init_otel_logging
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry_instrumentor_dramatiq import DramatiqInstrumentor

from .config import AppConfig

# Get the _tracer instance (You can set your own _tracer name)
tracer = trace.get_tracer(__name__)


def trace_function(trace_attributes: bool = True, trace_result: bool = True):
    """
    Decorator to trace callables using OpenTelemetry spans.

    Parameters:
    - trace_attributes (bool): If False, disables adding function arguments to the span.
    - trace_result (bool): If False, disables adding the function's result to the span.
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__) as span:
                try:
                    # Set function arguments as attributes
                    if trace_attributes:
                        span.set_attribute("function.args", str(args))
                        span.set_attribute("function.kwargs", str(kwargs))

                    result = await func(*args, **kwargs)
                    # Add result to span
                    if trace_result:
                        span.set_attribute("function.result", str(result))
                    return result
                except Exception as e:
                    # Record the exception in the span
                    span.record_exception(e)
                    span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
                    raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__) as span:
                try:
                    # Set function arguments as attributes
                    if trace_attributes:
                        span.set_attribute("function.args", str(args))
                        span.set_attribute("function.kwargs", str(kwargs))

                    result = func(*args, **kwargs)
                    # Add result to span
                    if trace_result:
                        span.set_attribute("function.result", str(result))
                    return result

                except Exception as e:
                    # Record the exception in the span
                    span.record_exception(e)
                    span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
                    raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


"""
Manual instrumentation bring several benefits:
- We don't need to use `opentelemetry-instrument` command, which
  gives us more control over the application running process.
- It is more performant
- It works with uvicorn reloader
- Avoids duplicating environment variables (i.e. OTEL_SERVICE_NAME is already defined in the config)
"""


def instrument_opentelemetry(config: AppConfig):  # pragma: no cover
    """
    Configures OpenTelemetry instrumentation for tracing, metrics, and logging.

    This function sets up OpenTelemetry components, including span processors, metric
    exporters, and log exporters, based on the provided application configuration.

    Parameters:
        config (AppConfig): Configuration object containing application-specific settings
        required for initializing OpenTelemetry instrumentation.
    """

    resource = Resource.create(
        {
            "service.name": config.APP_NAME,
            "deployment.environment": config.ENVIRONMENT,
        }
    )

    """
    The exporters can be still configured using OTEL_* environment variables,
    we capture and check the variables so we can avoid instrumenting if we don't have
    any endpoints configured. This will avoid instrumenting the application when
    running locally or during unit tests.
    """
    traces_endpoint = config.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT or config.OTEL_EXPORTER_OTLP_ENDPOINT
    metrics_endpoint = config.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT or config.OTEL_EXPORTER_OTLP_ENDPOINT
    logs_endpoint = config.OTEL_EXPORTER_OTLP_LOGS_ENDPOINT or config.OTEL_EXPORTER_OTLP_ENDPOINT

    # Traces
    if traces_endpoint:
        span_exporter = OTLPSpanExporter(endpoint=traces_endpoint)
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        trace.set_tracer_provider(tracer_provider)

    # Metrics
    if metrics_endpoint:
        metrics_exporter = OTLPMetricExporter(endpoint=metrics_endpoint)
        metrics_provider = MeterProvider(
            resource=resource, metric_readers=[PeriodicExportingMetricReader(metrics_exporter)]
        )
        metrics.set_meter_provider(metrics_provider)

    # Logs
    """
    Log instrumentation is still experimental, so we borrow a private instrumentation
    function, which should allow us to keep it working as expected with upcoming changes.
    When logs instrumentation will be stable this should be revisited.
    We still don't support passing the custom endpoint as parameter but it will
    be configured using OTEL_* environment variables.
    """
    if logs_endpoint:
        init_otel_logging(resource=resource, exporters={"otel": OTLPLogExporter})


def instrument_third_party():
    """
    Instrument third-party libraries for monitoring and tracing.

    This function initializes and instruments various third-party libraries
    that are commonly used in applications. It configures them to work with
    monitoring and tracing systems to collect performance metrics and
    distributed trace data.

    Raises:
        This function does not explicitly raise exceptions, but exceptions
        may propagate from the individual instrumentor methods if the
        instrumentation process fails.
    """
    DramatiqInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()
