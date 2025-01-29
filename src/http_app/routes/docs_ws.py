import json
from typing import Dict, Literal, List

import pydantic_asyncapi as pa
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from domains.books.events import BookCreatedV1, BookUpdatedV1

asyncapi_registry: Dict[str, Dict[Literal["receive", "send"], List]] = {
    "chat_channel": {
        "receive": [BookCreatedV1],
        "send": [BookUpdatedV1],
    }
}

components_schemas = {}

channels = {}
operations = {}

for channel, channel_operations in asyncapi_registry.items():
    _channel_messages = {}
    for operation, messages in channel_operations.items():
        _operation_message_refs = []
        for message in messages:
            # TODO: Check for overlapping model schemas, if they are different log a warning!
            components_schemas[message.__name__] = message.model_json_schema(
                mode="validation" if operation == "receive" else "serialization",
                ref_template="#/components/schemas/{model}"
            )
            components_schemas.update(message.model_json_schema(mode="serialization", ref_template="#/components/schemas/{model}")["$defs"])
            _channel_messages[message.__name__] = pa.v3.Message(
                payload=pa.v3.Reference(ref=f"#/components/schemas/{message.__name__}")
            )
            # Cannot point to the /components path
            _operation_message_refs.append(pa.v3.Reference(ref=f"#/channels/chat_channel/messages/{message.__name__}"))
        operations[operation] = pa.v3.Operation(
            action=operation,
            channel=pa.v3.Reference(ref=f"#/channels/{channel}"),
            messages=_operation_message_refs,
        )
    channels[channel] = pa.v3.Channel(
        title=channel,
        servers=[pa.v3.Reference(ref="#/servers/chat")],
        messages=_channel_messages,
    )



schema = pa.AsyncAPIV3(
    asyncapi="3.0.0",
    info=pa.v3.Info(
        title="Bookstore API",
        version="1.0.0",
        description="A bookstore aysncapi specification",
    ),
    components=pa.v3.Components(
        schemas=components_schemas,
    ),
    servers={
        "chat": pa.v3.Server(
            host="localhost",
            protocol="websocket",
        )
    },
    channels=channels,
    operations=operations,
)

router = APIRouter(prefix="/docs/ws")


@router.get(
    "/asyncapi.json",
    response_model_exclude_unset=True,
    include_in_schema=False,
)
def asyncapi_raw() -> pa.AsyncAPIV3:
    return schema


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
def get_asyncapi_html(
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
        # "schema": schema_json,
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
