from typing import Union

import socketio
from starlette.routing import Mount, Route, Router

from common import AppConfig, application_init
from common.di_container import Container
from common.telemetry import instrument_third_party
from socketio_app.namespaces.chat import ChatNamespace
from socketio_app.web_routes import docs

# These instrumentors patch and wrap libraries, we want
# to execute them ASAP
instrument_third_party()


def create_app(
    test_config: Union[AppConfig, None] = None,
    test_di_container: Union[Container, None] = None,
) -> Router:
    _config = test_config or AppConfig()
    ref = application_init(_config, test_di_container)
    ref.di_container.wire(packages=["socketio_app"])

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
