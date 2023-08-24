from typing import Union

from fastapi import FastAPI, Request
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from starlette.responses import JSONResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from structlog import get_logger

from config import AppConfig, init_logger
from domains import init_celery, init_domains
from gateways.storage import init_storage
from http_app.routes import init_routes


def create_app(
    test_config: Union[AppConfig, None] = None,
) -> FastAPI:
    app_config = test_config or AppConfig()
    init_logger(app_config)
    init_domains(app_config)
    app = FastAPI(debug=app_config.DEBUG)
    init_exception_handlers(app)

    init_storage()
    init_celery(app_config)
    init_routes(app)

    """
    OpenTelemetry prometheus exporter does not work together with automatic
    instrumentation, for now we keep the prometheus middleware even if
    having 2 different middlewares will add overhead.
    """
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics/", metrics)

    """
    OpenTelemetry middleware has to be the last one to make sure the
    tracing data handling is the outermost logic
    """
    app.add_middleware(OpenTelemetryMiddleware)

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
