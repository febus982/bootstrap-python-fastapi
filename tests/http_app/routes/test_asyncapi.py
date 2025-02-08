import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic_asyncapi.v3 import AsyncAPI, Info

fake_schema = AsyncAPI(
    asyncapi="3.0.0",
    info=Info(
        title="Some fake schema",
        version="1.2.3",
    ),
)


@patch("http_app.routes.asyncapi.get_schema", return_value=fake_schema)
async def test_asyncapi_json_is_whatever_returned_by_schema(
    mock_schema: MagicMock,
    testapp: FastAPI,
):
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get(
        "/asyncapi/asyncapi.json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.text == fake_schema.model_dump_json(exclude_unset=True)


@pytest.mark.parametrize("sidebar", (True, False))
@pytest.mark.parametrize("info", (True, False))
@pytest.mark.parametrize("servers", (True, False))
@pytest.mark.parametrize("operations", (True, False))
@pytest.mark.parametrize("messages", (True, False))
@pytest.mark.parametrize("schema", (True, False))
@pytest.mark.parametrize("errors", (True, False))
@pytest.mark.parametrize("expand_message_examples", (True, False))
async def test_ws_docs_renders_config_based_on_params(
    sidebar: bool,
    info: bool,
    servers: bool,
    operations: bool,
    messages: bool,
    schema: bool,
    errors: bool,
    expand_message_examples: bool,
    testapp: FastAPI,
):
    config = json.dumps(
        {
            "schema": {
                "url": "/asyncapi/asyncapi.json",
            },
            "config": {
                "show": {
                    "sidebar": sidebar,
                    "info": info,
                    "servers": servers,
                    "operations": operations,
                    "messages": messages,
                    "schemas": schema,
                    "errors": errors,
                },
                "expand": {
                    "messageExamples": expand_message_examples,
                },
                "sidebar": {
                    "showServers": "byDefault",
                    "showOperations": "byDefault",
                },
            },
        }
    )

    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get(
        "/asyncapi",
        params={
            "sidebar": sidebar,
            "info": info,
            "servers": servers,
            "operations": operations,
            "messages": messages,
            "schemas": schema,
            "errors": errors,
            "expand_message_examples": expand_message_examples,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert config in response.text
