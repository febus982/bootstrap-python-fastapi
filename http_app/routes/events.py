from fastapi import APIRouter
from enum import StrEnum

from domains.books import dto

router = APIRouter(prefix="/events")

_EVENT_REGISTRY: dict = {
    "book.created.v1": dto.Book.schema()
}

_EVENT_ENUM = StrEnum('_EVENT_ENUM', list(_EVENT_REGISTRY.keys()))


@router.get("/dataschemas/{event}")
async def event_schemas(event: _EVENT_ENUM):
    return _EVENT_REGISTRY.get(event, dict())

