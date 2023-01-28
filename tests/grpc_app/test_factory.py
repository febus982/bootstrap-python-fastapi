from unittest.mock import patch

from grpc.aio import Server

from config import AppConfig
from grpc_app import create_server


async def test_factory_returns_server():
    test_config = AppConfig(SQLALCHEMY_CONFIG={})

    with patch("grpc_app.init_storage", return_value=None):
        server = create_server(test_config=test_config)

    assert isinstance(server, Server)
