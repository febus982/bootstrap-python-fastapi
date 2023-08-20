import typing
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from domains.books.entities.events import BookCreatedV1

router = APIRouter(prefix="/events")


def _event_registry() -> Dict[str, typing.Type[BaseModel]]:
    return {"book.created.v1": BookCreatedV1}


@router.get("/dataschemas/{event}")
async def event_schema(event: str):
    event_model = _event_registry().get(event)
    if event_model:
        return event_model.model_json_schema(mode="serialization")
    else:
        raise HTTPException(status_code=404, detail="Schema not found")


@router.get("/dataschemas")
async def event_schema_list() -> List[str]:
    return list(_event_registry().keys())
