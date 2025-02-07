import json

from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from common import AppConfig
from common.asyncapi import get_schema


class PydanticResponse(JSONResponse):
    def render(self, content: BaseModel) -> bytes:
        return content.model_dump_json(
            exclude_unset=True,
        ).encode("utf-8")


async def asyncapi_json(request: Request) -> JSONResponse:
    return PydanticResponse(get_schema())


ASYNCAPI_COMPONENT_VERSION = "latest"

ASYNCAPI_JS_DEFAULT_URL = (
    f"https://unpkg.com/@asyncapi/react-component@{ASYNCAPI_COMPONENT_VERSION}/browser/standalone/index.js"
)
NORMALIZE_CSS_DEFAULT_URL = "https://cdn.jsdelivr.net/npm/modern-normalize/modern-normalize.min.css"
ASYNCAPI_CSS_DEFAULT_URL = (
    f"https://unpkg.com/@asyncapi/react-component@{ASYNCAPI_COMPONENT_VERSION}/styles/default.min.css"
)


# https://github.com/asyncapi/asyncapi-react/blob/v2.5.0/docs/usage/standalone-bundle.md
async def get_asyncapi_html(
    request: Request,
) -> HTMLResponse:
    app_config = AppConfig()
    """Generate HTML for displaying an AsyncAPI document."""
    config = {
        "schema": {
            "url": "/docs/asyncapi.json",
        },
        "config": {
            "show": {
                "sidebar": request.query_params.get("sidebar", "true") == "true",
                "info": request.query_params.get("info", "true") == "true",
                "servers": request.query_params.get("servers", "true") == "true",
                "operations": request.query_params.get("operations", "true") == "true",
                "messages": request.query_params.get("messages", "true") == "true",
                "schemas": request.query_params.get("schemas", "true") == "true",
                "errors": request.query_params.get("errors", "true") == "true",
            },
            "expand": {
                "messageExamples": request.query_params.get("expand_message_examples") == "true",
            },
            "sidebar": {
                "showServers": "byDefault",
                "showOperations": "byDefault",
            },
        },
    }

    return HTMLResponse(
        """
    <!DOCTYPE html>
    <html>
        <head>
    """
        f"""
        <title>{app_config.APP_NAME} AsyncAPI</title>
    """
        """
        <link rel="icon" href="https://www.asyncapi.com/favicon.ico">
        <link rel="icon" type="image/png" sizes="16x16" href="https://www.asyncapi.com/favicon-16x16.png">
        <link rel="icon" type="image/png" sizes="32x32" href="https://www.asyncapi.com/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="194x194" href="https://www.asyncapi.com/favicon-194x194.png">
    """
        f"""
        <link rel="stylesheet" href="{NORMALIZE_CSS_DEFAULT_URL}">
        <link rel="stylesheet" href="{ASYNCAPI_CSS_DEFAULT_URL}">
    """
        """
        </head>


        <body>
        <div id="asyncapi"></div>
    """
        f"""
        <script src="{ASYNCAPI_JS_DEFAULT_URL}"></script>
        <script>
    """
        f"""
            AsyncApiStandalone.render(
                {json.dumps(config)},
                document.getElementById('asyncapi')
            );
    """
        """
        </script>
        </body>
    </html>
    """
    )
