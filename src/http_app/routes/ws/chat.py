from typing import Optional, Sequence, Callable

from fastapi.types import DecoratedCallable
from typing_extensions import Annotated, Doc

from fastapi import APIRouter, params
from starlette.websockets import WebSocket, WebSocketDisconnect


class AsyncAPIEnabledRouter(APIRouter):
    def websocket(self, path: Annotated[
        str,
        Doc(
            """
            WebSocket path.
            """
        ),
    ], name: Annotated[
        Optional[str],
        Doc(
            """
            A name for the WebSocket. Only used internally.
            """
        ),
    ] = None, *, dependencies: Annotated[
        Optional[Sequence[params.Depends]],
        Doc(
            """
            A list of dependencies (using `Depends()`) to be used for this
            WebSocket.

            Read more about it in the
            [FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).
            """
        ),
    ] = None) -> Callable[[DecoratedCallable], DecoratedCallable]:
        route = super().websocket(path, name, dependencies=dependencies)
        return route


router = AsyncAPIEnabledRouter(prefix="/chat")

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
