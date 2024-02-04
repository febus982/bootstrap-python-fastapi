from collections.abc import Iterator
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from http_app import create_app


@pytest.fixture(scope="function")
def testapp(test_config) -> Iterator[FastAPI]:
    # We don't need the storage to test the HTTP app
    with patch("bootstrap.bootstrap.init_storage", return_value=None):
        app = create_app(test_config=test_config)
        yield app
