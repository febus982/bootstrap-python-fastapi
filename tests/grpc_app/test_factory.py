from unittest.mock import patch

import pytest
from grpc.aio import Server

from config import AppConfig
from grpc_app import create_server


@pytest.mark.parametrize("test_config", [AppConfig(SQLALCHEMY_CONFIG={}), None])
async def test_factory_returns_server(test_config):
    with patch("grpc_app.init_storage", return_value=None):
        server = create_server(test_config=test_config)

    assert isinstance(server, Server)
