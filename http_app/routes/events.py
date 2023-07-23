from enum import StrEnum

from fastapi import APIRouter

from domains.books.entities.events import BookCreatedV1Data

router = APIRouter(prefix="/events")

_EVENT_REGISTRY: dict = {"book.created.v1": BookCreatedV1Data.schema()}

_EVENT_ENUM = StrEnum(  # type: ignore # no dynamic lists
    "_EVENT_ENUM", list(_EVENT_REGISTRY.keys())
)


@router.get("/dataschemas/{event}")
async def event_schemas(event: _EVENT_ENUM):
    return _EVENT_REGISTRY.get(event, dict())
