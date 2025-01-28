import json

import pydantic_asyncapi as pa
from fastapi import APIRouter
from starlette.responses import HTMLResponse

schema = pa.AsyncAPIV3(
    asyncapi="3.0.0",
    info=pa.v3.Info(
        title="Bookstore API",
        version="1.0.0",
        description="test",
    ),
)

router = APIRouter(prefix="/docs")

@router.get("/asyncapi.json", response_model_exclude_unset=True)
def asyncapi_raw() -> pa.AsyncAPIV3:
    return schema

ASYNCAPI_JS_DEFAULT_URL = "https://unpkg.com/@asyncapi/react-component@2.5.0/browser/standalone/index.js"
NORMALIZE_CSS_DEFAULT_URL = "https://cdn.jsdelivr.net/npm/modern-normalize/modern-normalize.min.css"
ASYNCAPI_CSS_DEFAULT_URL = (
    "https://unpkg.com/@asyncapi/react-component@2.5.0/styles/default.min.css"
)


# https://github.com/asyncapi/asyncapi-react/blob/v2.5.0/docs/usage/standalone-bundle.md
@router.get("/asyncapi")
def get_asyncapi_html(
    sidebar: bool = True,
    info: bool = True,
    servers: bool = True,
    operations: bool = True,
    messages: bool = True,
    schemas: bool = True,
    errors: bool = True,
    expand_message_examples: bool = True,
    title: str = "Bookstore API",
) -> HTMLResponse:
    """Generate HTML for displaying an AsyncAPI document."""
    schema_json = schema.model_dump_json(exclude_unset=True)

    config = {
        "schema": schema_json,
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

    return HTMLResponse("""
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
            AsyncApiStandalone.render({json.dumps(config)}, document.getElementById('asyncapi'));
    """
        """
        </script>
        </body>
    </html>
    """
    )
