from fastapi import FastAPI

from http_app.routes import api, graphql, hello, ping, events


def init_routes(app: FastAPI) -> None:
    app.include_router(api.router)
    app.include_router(ping.router)
    app.include_router(hello.router)
    app.include_router(events.router)
    app.include_router(graphql.router, prefix="/graphql")
