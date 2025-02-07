import json
from typing import Annotated

import pydantic_asyncapi as pa
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import HTMLResponse

from common import AppConfig
from common.asyncapi import get_schema
from http_app.dependencies import get_app_config

router = APIRouter(prefix="/asyncapi")


@router.get(
    "/asyncapi.json",
    response_model_exclude_unset=True,
    include_in_schema=False,
)
def asyncapi_raw() -> pa.v3.AsyncAPI:
    return get_schema()


ASYNCAPI_COMPONENT_VERSION = "latest"

ASYNCAPI_JS_DEFAULT_URL = (
    f"https://unpkg.com/@asyncapi/react-component@{ASYNCAPI_COMPONENT_VERSION}/browser/standalone/index.js"
)
NORMALIZE_CSS_DEFAULT_URL = "https://cdn.jsdelivr.net/npm/modern-normalize/modern-normalize.min.css"
ASYNCAPI_CSS_DEFAULT_URL = (
    f"https://unpkg.com/@asyncapi/react-component@{ASYNCAPI_COMPONENT_VERSION}/styles/default.min.css"
)


# https://github.com/asyncapi/asyncapi-react/blob/v2.5.0/docs/usage/standalone-bundle.md
@router.get("")
async def get_asyncapi_html(
    app_config: Annotated[AppConfig, Depends(get_app_config)],
    sidebar: bool = True,
    info: bool = True,
    servers: bool = True,
    operations: bool = True,
    messages: bool = True,
    schemas: bool = True,
    errors: bool = True,
    expand_message_examples: bool = False,
) -> HTMLResponse:
    """Generate HTML for displaying an AsyncAPI document."""
    config = {
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
                "schemas": schemas,
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
