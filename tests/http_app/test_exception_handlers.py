from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from common.errors import ApplicationError


@patch("logging.exception")
async def test_unhandled_exception_is_logged_handler_returns_500(
    mocked_logging_exception: MagicMock,
    testapp: FastAPI,
):
    my_exc = Exception("Some random exception")

    @testapp.get("/unhandled_exception")
    async def fake_endpoint():
        raise my_exc

    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/unhandled_exception")

    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}
    mocked_logging_exception.assert_called_once_with(my_exc)


@patch("logging.exception")
async def test_application_error_is_logged_handler_returns_500(
    mocked_logging_exception: MagicMock,
    testapp: FastAPI,
):
    my_exc = ApplicationError(
        public_message="Some random exception",
        internal_message="Some random internal exception",
        code="ERR_1234567890",
        metadata={
            "user_id": "1234567890",
        },
    )

    @testapp.get("/application_error")
    async def fake_endpoint():
        raise my_exc

    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/application_error")

    assert response.status_code == 500
    assert response.json() == {"error": {"code": "ERR_1234567890", "message": "Some random exception"}}
    mocked_logging_exception.assert_called_once_with(
        my_exc.internal_message, extra={"code": my_exc.code, "metadata": my_exc.metadata}
    )
