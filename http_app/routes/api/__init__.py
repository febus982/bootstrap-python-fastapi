from fastapi import APIRouter

from . import books

router = APIRouter(prefix="/api")

router.include_router(books.router_v1)
router.include_router(books.router_v2)
