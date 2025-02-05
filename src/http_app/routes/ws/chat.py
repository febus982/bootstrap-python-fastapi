from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from common.asyncapi import (
    register_channel,
    register_channel_operation,
    register_server,
)
from domains.books.events import BookUpdatedV1

router = APIRouter(prefix="/chat")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


"""
In websocket case we create a server per route.
If we create other routes we can create more servers
"""
register_server(
    id="chat",
    # TODO: Inject host using config?
    host="localhost/endpoint",
    protocol="ws",
)
register_channel(
    id="ChatChannel",
    address="chat",
    title="Chat channel",
    description="A channel supporting send and receive chat messages between clients",
    server_id="chat",
)
register_channel_operation(
    channel_id="ChatChannel",
    operation_type="send",
    messages=[BookUpdatedV1],
    operation_name="SendMessage",
)
register_channel_operation(
    channel_id="ChatChannel",
    operation_type="receive",
    messages=[BookUpdatedV1],
    operation_name="ReceiveMessage",
)
