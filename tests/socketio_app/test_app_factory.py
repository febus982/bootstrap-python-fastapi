from unittest.mock import patch

import socketio
from starlette.routing import Mount, Router

from common import AppConfig
from socketio_app import create_app


def test_create_app_returns_router():
    """Test that create_app returns a Router instance"""
    app = create_app()
    assert isinstance(app, Router)


def test_create_app_with_custom_config():
    """Test that create_app accepts custom config"""
    test_config = AppConfig(DEBUG=True)
    with patch("common.bootstrap.init_storage", return_value=None):
        app = create_app(test_config=test_config)

    assert isinstance(app, Router)


def test_create_app_routes():
    """Test that create_app creates all expected routes"""
    with patch("common.bootstrap.init_storage", return_value=None):
        app = create_app()

    # Check that we have exactly 3 routes (docs JSON, docs HTML, and socketio mount)
    assert len(app.routes) == 3

    # Check routes paths and methods
    routes = [(route.path, getattr(route, "methods", None)) for route in app.routes]
    assert ("/docs/asyncapi.json", {"GET", "HEAD"}) in routes
    assert ("/docs", {"GET", "HEAD"}) in routes

    # Check that one route is a Mount instance for socketio
    mount_routes = [route for route in app.routes if isinstance(route, Mount)]
    assert len(mount_routes) == 1
    assert mount_routes[0].name == "socketio"
    assert isinstance(mount_routes[0].app, socketio.ASGIApp)


def test_create_app_socketio_namespace():
    """Test that socketio server has the chat namespace registered"""
    with patch("common.bootstrap.init_storage", return_value=None):
        app = create_app()

    # Find the socketio mount
    socketio_mount = next(route for route in app.routes if isinstance(route, Mount))
    sio_app = socketio_mount.app

    # Check that the chat namespace is registered
    assert "/chat" in sio_app.engineio_server.namespace_handlers
