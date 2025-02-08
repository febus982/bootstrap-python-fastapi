from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel
from starlette.requests import Request

from socketio_app.web_routes.docs import (
    ASYNCAPI_CSS_DEFAULT_URL,
    ASYNCAPI_JS_DEFAULT_URL,
    NORMALIZE_CSS_DEFAULT_URL,
    PydanticResponse,
    asyncapi_json,
    get_asyncapi_html,
)


# Test model
class TestModel(BaseModel):
    name: str
    value: int


# Fixtures
@pytest.fixture
def test_model():
    return TestModel(name="test", value=42)


@pytest.fixture
def mock_request():
    return Mock(spec=Request)


@pytest.fixture
def mock_app_config():
    with patch("socketio_app.web_routes.docs.AppConfig") as mock:
        mock.return_value.APP_NAME = "Test App"
        yield mock


# Tests for PydanticResponse
def test_pydantic_response_render(test_model):
    response = PydanticResponse(test_model)
    expected = b'{"name":"test","value":42}'
    assert response.render(test_model) == expected


# Tests for asyncapi_json endpoint
async def test_asyncapi_json(mock_request, test_model):
    with patch("socketio_app.web_routes.docs.get_schema") as mock_get_schema:
        mock_get_schema.return_value = test_model
        response = await asyncapi_json(mock_request)
        assert isinstance(response, PydanticResponse)
        assert response.body == b'{"name":"test","value":42}'


# Tests for get_asyncapi_html endpoint
async def test_get_asyncapi_html_default_params(mock_request, mock_app_config):
    mock_request.query_params = {}
    response = await get_asyncapi_html(mock_request)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    content = response.body.decode()
    assert "Test App AsyncAPI" in content
    assert ASYNCAPI_JS_DEFAULT_URL in content
    assert NORMALIZE_CSS_DEFAULT_URL in content
    assert ASYNCAPI_CSS_DEFAULT_URL in content
    assert '"sidebar": true' in content
    assert '"info": true' in content


async def test_get_asyncapi_html_custom_params(mock_request, mock_app_config):
    mock_request.query_params = {
        "sidebar": "false",
        "info": "false",
        "servers": "false",
        "operations": "false",
        "messages": "false",
        "schemas": "false",
        "errors": "false",
        "expand_message_examples": "true",
    }

    response = await get_asyncapi_html(mock_request)
    content = response.body.decode()

    assert '"sidebar": false' in content
    assert '"info": false' in content
    assert '"servers": false' in content
    assert '"operations": false' in content
    assert '"messages": false' in content
    assert '"schemas": false' in content
    assert '"errors": false' in content
    assert '"messageExamples": true' in content
