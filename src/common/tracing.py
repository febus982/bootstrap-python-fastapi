import asyncio
from functools import wraps
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def trace_function(trace_attributes: bool = True, trace_result: bool = True):
    """
    Decorator to trace callables using OpenTelemetry spans.

    Parameters:
    - trace_attributes (bool): If False, disables adding function arguments to the span.
    - trace_result (bool): If False, disables adding the function's result to the span.
    """

    def set_span_attributes(span, args, kwargs, result=None):
        """Helper to set function arguments and results as span attributes."""
        if trace_attributes:
            span.set_attribute("function.args", str(args))
            span.set_attribute("function.kwargs", str(kwargs))
        if trace_result and result is not None:
            span.set_attribute("function.result", str(result))

    def record_exception(span, exception):
        """Helper to handle exception recording in a span."""
        span.record_exception(exception)
        span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))

    async def handle_async(span, func, *args, **kwargs):
        """Handle asynchronous functions."""
        try:
            result = await func(*args, **kwargs)
            set_span_attributes(span, args, kwargs, result)
            return result
        except Exception as e:
            record_exception(span, e)
            raise

    def handle_sync(span, func, *args, **kwargs):
        """Handle synchronous functions."""
        try:
            result = func(*args, **kwargs)
            set_span_attributes(span, args, kwargs, result)
            return result
        except Exception as e:
            record_exception(span, e)
            raise

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__) as span:
                if asyncio.iscoroutinefunction(func):
                    return handle_async(span, func, *args, **kwargs)
                return handle_sync(span, func, *args, **kwargs)

        return wrapper

    return decorator
