from collections.abc import Iterator
from unittest.mock import patch

import pytest
from dependency_injector.providers import Object
from starlette.routing import Router

from common.di_container import Container
from socketio_app import create_app


@pytest.fixture(scope="session")
def test_di_container(test_config) -> Container:
    return Container(
        config=Object(test_config),
    )


@pytest.fixture(scope="session")
def testapp(test_config, test_di_container) -> Iterator[Router]:
    # We don't need the storage to test the HTTP app
    with patch("common.bootstrap.init_storage", return_value=None):
        app = create_app(test_config=test_config, test_di_container=test_di_container)
        yield app
