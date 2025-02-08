from typing import Union

import socketio
from starlette.routing import Mount, Route, Router

from common import AppConfig, application_init
from socketio_app.namespaces.chat import ChatNamespace
from socketio_app.web_routes import docs


def create_app(
    test_config: Union[AppConfig, None] = None,
) -> Router:
    _config = test_config or AppConfig()
    application_init(_config)

    # SocketIO App
    sio = socketio.AsyncServer(async_mode="asgi")
    # Namespaces are the equivalent of Routes.
    sio.register_namespace(ChatNamespace("/chat"))

    # Render /docs endpoint using starlette, and all the rest handled with Socket.io
    routes = [
        Route("/docs/asyncapi.json", docs.asyncapi_json, methods=["GET"]),
        Route("/docs", docs.get_asyncapi_html, methods=["GET"]),
        Mount("", app=socketio.ASGIApp(sio), name="socketio"),
    ]

    # No need for whole starlette, we're rendering a simple couple of endpoints
    # https://www.starlette.io/routing/#working-with-router-instances
    app = Router(routes=routes)

    return app
