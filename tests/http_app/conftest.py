from collections.abc import Iterator
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from http_app import create_app


@pytest.fixture(scope="function")
def testapp(test_config, test_container) -> Iterator[FastAPI]:
    # We don't need the storage to test the HTTP app
    with patch("http_app.init_storage", return_value=None):
        app = create_app(
            test_config=test_config,
            test_di_container=test_container,
        )
        yield app
