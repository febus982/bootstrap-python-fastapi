from unittest.mock import AsyncMock, patch

import pytest

from socketio_app import ChatNamespace


@pytest.fixture
def chat_namespace():
    return ChatNamespace("/chat")


async def test_on_connect(chat_namespace):
    sid = "test_session_id"
    environ = {}

    # Test that connect doesn't raise any exceptions
    chat_namespace.on_connect(sid, environ)


async def test_on_disconnect(chat_namespace):
    sid = "test_session_id"
    reason = "test_reason"

    # Test that disconnect doesn't raise any exceptions
    chat_namespace.on_disconnect(sid, reason)


async def test_on_echo_message(chat_namespace):
    sid = "test_session_id"
    test_data = {"message": "Hello, World!"}

    # Mock the emit method
    chat_namespace.emit = AsyncMock()

    # Mock the logging
    with patch("logging.info") as mock_log:
        await chat_namespace.on_echo_message(sid, test_data)

        # Verify logging was called
        mock_log.assert_called_once_with("received message")

        # Verify emit was called with correct arguments
        chat_namespace.emit.assert_called_once_with("echo_response", test_data)
