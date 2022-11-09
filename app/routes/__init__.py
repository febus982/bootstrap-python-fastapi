from fastapi import FastAPI

from app.routes.ping import router as ping_router


def init_routes(app: FastAPI) -> None:
    app.include_router(ping_router)
