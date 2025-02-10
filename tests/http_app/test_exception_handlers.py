from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient


@patch("logging.exception")
async def test_exception_is_logged_handler_returns_500(
    mocked_logging_exception: MagicMock,
    testapp: FastAPI,
):
    my_exc = Exception("Some random exception")

    @testapp.get("/ppp")
    async def fake_endpoint():
        raise my_exc

    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/ppp")

    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}
    mocked_logging_exception.assert_called_once_with(my_exc)
