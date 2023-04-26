from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

from http_app.routes.api.books import router as api_books_router
from http_app.routes.hello import router as hello_router
from http_app.routes.ping import router as ping_router


def init_versioned_routes(app: FastAPI) -> None:
    app.include_router(api_books_router)


def init_unversioned_routes(app: FastAPI) -> None:
    app.include_router(ping_router)
    app.include_router(hello_router)

    @app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
    async def get_api_versions() -> HTMLResponse:
        """
        Swagger page for non-versioned routes.
        """

        return get_swagger_ui_html(  # pragma: no cover
            openapi_url=f"{app.openapi_url}",
            title=f"{app.title}",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        )
