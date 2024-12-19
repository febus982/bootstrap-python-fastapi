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
        def sync_or_async_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__) as span:
                try:
                    # Set function arguments as attributes
                    if trace_attributes:
                        span.set_attribute("function.args", str(args))
                        span.set_attribute("function.kwargs", str(kwargs))

                    async def async_handler():
                        result = await func(*args, **kwargs)
                        # Add result to span
                        if trace_result:
                            span.set_attribute("function.result", str(result))
                        return result

                    def sync_handler():
                        result = func(*args, **kwargs)
                        # Add result to span
                        if trace_result:
                            span.set_attribute("function.result", str(result))
                        return result

                    if asyncio.iscoroutinefunction(func):
                        return async_handler()
                    else:
                        return sync_handler()

                except Exception as e:
                    # Record the exception in the span
                    span.record_exception(e)
                    span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
                    raise

        return sync_or_async_wrapper

    return decorator
