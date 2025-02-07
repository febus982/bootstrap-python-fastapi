from fastapi import FastAPI

from http_app.routes import (
    api,
    asyncapi,
    events,
    graphql,
    hello,
    ping,
    user_registered_hook,
)


def init_routes(app: FastAPI) -> None:
    app.include_router(api.router)
    app.include_router(asyncapi.router)
    app.include_router(ping.router)
    app.include_router(hello.router)
    app.include_router(events.router)
    app.include_router(user_registered_hook.router)
    app.include_router(graphql.router, prefix="/graphql")
