from collections.abc import Iterator
from unittest.mock import patch

import pytest
from dependency_injector.providers import Object
from fastapi import FastAPI

from common.di_container import Container
from http_app import create_app


@pytest.fixture(scope="session")
def test_di_container(test_config) -> Container:
    return Container(
        config=Object(test_config),
    )


@pytest.fixture(scope="session")
def testapp(test_config, test_di_container) -> Iterator[FastAPI]:
    # We don't need the storage to test the HTTP app
    with patch("common.bootstrap.init_storage", return_value=None):
        app = create_app(test_config=test_config, test_di_container=test_di_container)
        yield app
