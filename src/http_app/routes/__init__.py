from fastapi import FastAPI

from http_app.routes import api, events, graphql, hello, ping, user_registered_hook, asyncapi_docs


def init_routes(app: FastAPI) -> None:
    app.include_router(api.router)
    app.include_router(asyncapi_docs.router)
    app.include_router(ping.router)
    app.include_router(hello.router)
    app.include_router(events.router)
    app.include_router(user_registered_hook.router)
    app.include_router(graphql.router, prefix="/graphql")
