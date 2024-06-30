from contextlib import asynccontextmanager
from typing import Any, Union

from bootstrap import AppConfig, application_init
from fastapi import FastAPI, Request
from faststream.broker.core.usecase import BrokerUsecase
from faststream.types import Lifespan
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from starlette.responses import JSONResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from structlog import get_logger

from http_app.routes import init_routes


def create_app(
    test_config: Union[AppConfig, None] = None,
) -> FastAPI:
    app_config = test_config or AppConfig()
    ref = application_init(app_config)

    """
    We don't want to couple together FastAPI and FastStream
    so we use a lifespan handler instead of the plugin to
    remain decoupled but still able use any generic broker
    for message publishing in FastAPI.
    """
    app = FastAPI(
        debug=app_config.DEBUG,
        title=app_config.APP_NAME,
        lifespan=faststream_lifespan(ref.faststream_broker),
    )
    init_exception_handlers(app)

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
    Some typing issues to be addressed in OpenTelemetry but it works.
    """
    app.add_middleware(OpenTelemetryMiddleware)  # type: ignore

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


def faststream_lifespan(broker: BrokerUsecase[Any, Any]) -> Lifespan:
    @asynccontextmanager
    async def handler(app: FastAPI):
        await broker.start()
        try:
            yield
        finally:
            await broker.close()

    return handler
