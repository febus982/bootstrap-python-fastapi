from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from domains.books.entities.events import BookCreatedV1Data

router = APIRouter(prefix="/events")


def _event_registry() -> Dict[str, Any]:
    return {"book.created.v1": BookCreatedV1Data.schema()}


@router.get("/dataschemas/{event}")
async def event_schema(event: str):
    schema = _event_registry().get(event)
    if schema:
        return schema
    else:
        raise HTTPException(status_code=404, detail="Schema not found")


@router.get("/dataschemas")
async def event_schema_list() -> List[str]:
    return list(_event_registry().keys())
