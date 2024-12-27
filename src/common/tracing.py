import asyncio
from functools import wraps

from opentelemetry import trace

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
