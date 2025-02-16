import asyncio
from unittest.mock import MagicMock, call, patch

import pytest

from common.telemetry import trace_function


@pytest.fixture
def mock_tracer():
    """
    Fixture to mock the OpenTelemetry tracer and span.
    """
    mock_tracer = MagicMock()
    mock_span = MagicMock()
    mock_tracer.start_as_current_span.return_value.__enter__.return_value = mock_span

    with (
        patch("opentelemetry.trace.get_tracer", return_value=mock_tracer),
        patch("common.telemetry.tracer", mock_tracer),
    ):
        yield mock_tracer, mock_span


def test_sync_function_default_params(mock_tracer):
    """
    Test a synchronous function with default decorator parameters.
    """
    mock_tracer, mock_span = mock_tracer

    # Define a sync function to wrap with the decorator
    @trace_function()
    def add_nums(a, b):
        return a + b

    # Call the function
    result = add_nums(2, 3)

    # Assertions
    assert result == 5
    mock_tracer.start_as_current_span.assert_called_once_with("add_nums")
    mock_span.set_attribute.assert_any_call("function.args", "(2, 3)")
    mock_span.set_attribute.assert_any_call("function.result", "5")


async def test_async_function_default_params(mock_tracer):
    """
    Test an asynchronous function with default decorator parameters.
    """
    mock_tracer, mock_span = mock_tracer

    # Define an async function to wrap with the decorator
    @trace_function()
    async def async_func(a, b):
        await asyncio.sleep(0.1)
        return a * b

    # Run the async function
    result = await async_func(4, 5)

    # Assertions
    assert result == 20
    mock_tracer.start_as_current_span.assert_called_once_with("async_func")
    mock_span.set_attribute.assert_any_call("function.args", "(4, 5)")
    mock_span.set_attribute.assert_any_call("function.result", "20")


def test_disable_function_attributes_sync(mock_tracer):
    """
    Test a synchronous function with `add_function_attributes` set to False.
    """
    mock_tracer, mock_span = mock_tracer

    # Define a sync function with attributes disabled
    @trace_function(trace_attributes=False)
    def sync_func(a, b):
        return a - b

    # Call the function
    result = sync_func(10, 6)

    # Assertions
    assert result == 4
    mock_tracer.start_as_current_span.assert_called_once_with("sync_func")
    mock_span.set_attribute.assert_any_call("function.result", "4")
    assert call("function.args", "(10, 6)") not in mock_span.set_attribute.call_args_list


async def test_disable_function_attributes_async(mock_tracer):
    """
    Test an asynchronous function with `add_function_attributes` set to False.
    """
    mock_tracer, mock_span = mock_tracer

    # Define a sync function with attributes disabled
    @trace_function(trace_attributes=False)
    async def async_func(a, b):
        return a - b

    # Call the function
    result = await async_func(10, 6)

    # Assertions
    assert result == 4
    mock_tracer.start_as_current_span.assert_called_once_with("async_func")
    mock_span.set_attribute.assert_any_call("function.result", "4")
    assert call("function.args", "(10, 6)") not in mock_span.set_attribute.call_args_list


def test_disable_result_in_span_sync(mock_tracer):
    """
    Test an asynchronous function with `add_result_to_span` set to False.
    """
    mock_tracer, mock_span = mock_tracer

    # Define an async function with result disabled
    @trace_function(trace_result=False)
    def sync_func(a, b):
        return a / b

    # Run the async function
    result = sync_func(10, 2)

    # Assertions
    assert result == 5.0
    mock_tracer.start_as_current_span.assert_called_once_with("sync_func")
    mock_span.set_attribute.assert_any_call("function.args", "(10, 2)")
    assert call("function.result") not in mock_span.set_attribute.call_args_list


async def test_disable_result_in_span(mock_tracer):
    """
    Test an asynchronous function with `add_result_to_span` set to False.
    """
    mock_tracer, mock_span = mock_tracer

    # Define an async function with result disabled
    @trace_function(trace_result=False)
    async def async_func(a, b):
        await asyncio.sleep(0.1)
        return a / b

    # Run the async function
    result = await async_func(10, 2)

    # Assertions
    assert result == 5.0
    mock_tracer.start_as_current_span.assert_called_once_with("async_func")
    mock_span.set_attribute.assert_any_call("function.args", "(10, 2)")
    assert call("function.result") not in mock_span.set_attribute.call_args_list


def test_exception_in_function_sync(mock_tracer):
    """
    Test behavior when the function raises an exception.
    """
    mock_tracer, mock_span = mock_tracer

    # Define a failing function
    @trace_function()
    def failing_func(a, b):
        if b == 0:
            raise ValueError("Division by zero!")
        return a / b

    # Use pytest to assert the exception is raised
    with pytest.raises(ValueError, match="Division by zero!"):
        failing_func(10, 0)

    # Assertions
    mock_tracer.start_as_current_span.assert_called_once_with("failing_func")
    mock_span.record_exception.assert_called_once()
    mock_span.set_status.assert_called_once()


async def test_exception_in_function_async(mock_tracer):
    """
    Test behavior when the function raises an exception.
    """
    mock_tracer, mock_span = mock_tracer

    # Define a failing function
    @trace_function()
    async def failing_func(a, b):
        if b == 0:
            raise ValueError("Division by zero!")
        return a / b

    # Use pytest to assert the exception is raised
    with pytest.raises(ValueError, match="Division by zero!"):
        await failing_func(10, 0)

    # Assertions
    mock_tracer.start_as_current_span.assert_called_once_with("failing_func")
    mock_span.record_exception.assert_called_once()
    mock_span.set_status.assert_called_once()
