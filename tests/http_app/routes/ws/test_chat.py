import pytest
from fastapi.testclient import TestClient

from http_app.routes.ws.chat import ConnectionManager


@pytest.fixture
def test_client(testapp):
    return TestClient(testapp)


@pytest.fixture
def connection_manager():
    return ConnectionManager()


def test_websocket_connection(test_client):
    with test_client.websocket_connect("/ws/chat/1") as websocket:
        websocket.send_text("Hello!")
        data = websocket.receive_text()

        assert data == "You wrote: Hello!"
        broadcast = websocket.receive_text()
        assert broadcast == "Client #1 says: Hello!"


def test_multiple_clients(test_client):
    with test_client.websocket_connect("/ws/chat/1") as websocket1:
        with test_client.websocket_connect("/ws/chat/2") as websocket2:
            # Client 1 sends message
            websocket1.send_text("Hello from client 1")

            # Client 1 receives personal message
            data1 = websocket1.receive_text()
            assert data1 == "You wrote: Hello from client 1"

            # Both clients receive broadcast
            broadcast1 = websocket1.receive_text()
            broadcast2 = websocket2.receive_text()
            assert broadcast1 == "Client #1 says: Hello from client 1"
            assert broadcast2 == "Client #1 says: Hello from client 1"


def test_client_disconnect(test_client):
    with test_client.websocket_connect("/ws/chat/1") as websocket1:
        with test_client.websocket_connect("/ws/chat/2") as websocket2:
            # Close first client
            websocket1.close()

            # Second client should receive disconnect message
            disconnect_message = websocket2.receive_text()
            assert disconnect_message == "Client #1 left the chat"


@pytest.mark.asyncio
async def test_connection_manager():
    manager = ConnectionManager()

    # Mock WebSocket for testing
    class MockWebSocket:
        def __init__(self):
            self.received_messages = []

        async def accept(self):
            pass

        async def send_text(self, message: str):
            self.received_messages.append(message)

    # Test connect
    websocket = MockWebSocket()
    await manager.connect(websocket)
    assert len(manager.active_connections) == 1

    # Test personal message
    await manager.send_personal_message("test message", websocket)
    assert websocket.received_messages[-1] == "test message"

    # Test broadcast
    await manager.broadcast("broadcast message")
    assert websocket.received_messages[-1] == "broadcast message"

    # Test disconnect
    manager.disconnect(websocket)
    assert len(manager.active_connections) == 0
