from fastapi import APIRouter

from . import chat

router = APIRouter(prefix="/ws")
router.include_router(chat.router)