from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from httpx import AsyncClient


@patch("http_app.get_logger")
async def test_exception_is_logged_handler_returns_500(
    mocked_get_logger: MagicMock,
    testapp: FastAPI,
):
    my_exc = Exception("Some random exception")

    @testapp.get("/ppp")
    async def fake_endpoint():
        raise my_exc

    mocked_get_logger.return_value.exception = MagicMock(return_value=None)

    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.get("/ppp")

    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}
    mocked_get_logger.assert_called_once()
    mocked_get_logger.return_value.exception.assert_called_once_with(my_exc)
