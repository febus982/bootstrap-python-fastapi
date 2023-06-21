from typing import Union

from fastapi import FastAPI, Request
from fastapi_versionizer import versionize
from starlette.responses import JSONResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from structlog import get_logger

from config import AppConfig, init_logger
from domains import init_domains
from http_app.routes import init_unversioned_routes, init_versioned_routes
from storage import init_storage


def create_app(
    test_config: Union[AppConfig, None] = None,
) -> FastAPI:
    app_config = test_config or AppConfig()
    init_logger(app_config)
    init_domains(app_config)
    app = FastAPI(debug=app_config.DEBUG)
    init_exception_handlers(app)

    init_storage()

    app.add_middleware(PrometheusMiddleware)

    init_versioned_routes(app)
    versionize(
        app=app,
        prefix_format="/api/v{major}",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    """
    Routes initalised after `versionize` are not versioned
    """
    init_unversioned_routes(app)
    app.add_route("/metrics/", metrics)

    return app


def init_exception_handlers(app: FastAPI) -> None:
    # This is a catch-all middleware for unhandled exceptions
    # other Exception handlers should be initialised using
    # the @app.exception_handler decorator
    # https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
    @app.middleware("http")
    async def add_exception_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger = get_logger(__name__)
            await logger.aexception(e)
            return JSONResponse({"error": "Internal server error"}, status_code=500)
