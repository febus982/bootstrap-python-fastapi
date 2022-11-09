from fastapi import FastAPI

from app.routes.ping import router as ping_router
from app.routes.books import router as books_router


def init_routes(app: FastAPI) -> None:
    app.include_router(ping_router)
    app.include_router(books_router)
