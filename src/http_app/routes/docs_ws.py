import json

import pydantic_asyncapi as pa
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from common.asyncapi import add_channel_to_asyncapi_schema, get_asyncapi_schema
from domains.books.events import BookCreatedV1, BookUpdatedV1


router = APIRouter(prefix="/docs/ws")


@router.get(
    "/asyncapi.json",
    response_model_exclude_unset=True,
    include_in_schema=False,
)
@add_channel_to_asyncapi_schema(send=[BookUpdatedV1])
def asyncapi_raw() -> pa.v3.AsyncAPI:
    return get_asyncapi_schema()


ASYNCAPI_COMPONENT_VERSION = "latest"

ASYNCAPI_JS_DEFAULT_URL = (
    f"https://unpkg.com/@asyncapi/react-component@{ASYNCAPI_COMPONENT_VERSION}/browser/standalone/index.js"
)
NORMALIZE_CSS_DEFAULT_URL = (
    "https://cdn.jsdelivr.net/npm/modern-normalize/modern-normalize.min.css"
)
ASYNCAPI_CSS_DEFAULT_URL = (
    f"https://unpkg.com/@asyncapi/react-component@{ASYNCAPI_COMPONENT_VERSION}/styles/default.min.css"
)


# https://github.com/asyncapi/asyncapi-react/blob/v2.5.0/docs/usage/standalone-bundle.md
@router.get("", include_in_schema=False)
@add_channel_to_asyncapi_schema(receive=[BookCreatedV1], send=[BookUpdatedV1])
async def get_asyncapi_html(
    sidebar: bool = True,
    info: bool = True,
    servers: bool = True,
    operations: bool = True,
    messages: bool = True,
    schemas: bool = True,
    errors: bool = True,
    expand_message_examples: bool = False,
    title: str = "Websocket",
) -> HTMLResponse:

    """Generate HTML for displaying an AsyncAPI document."""
    config = {
        "schema": {
            "url": "/docs/ws/asyncapi.json",
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
        <title>{title} AsyncAPI</title>
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
