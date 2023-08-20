import typing
from typing import Any, Dict, List

from fastapi import APIRouter, Body, Header, HTTPException
from pydantic import BaseModel

from domains.books.entities.events import BookCreatedV1

router = APIRouter(prefix="/events")

_EVENTS_UNION_TYPE = typing.Union[BookCreatedV1]


def _event_registry() -> Dict[str, typing.Type[BaseModel]]:
    return {
        "book.created.v1": BookCreatedV1,
        # If we find a way to read the class type from here
        # we can reduce duplication in this way:
        #
        # event.type: event
        # for event in typing.get_args(_EVENTS_UNION_TYPE)
    }


def _event_schema_examples() -> dict[str, dict[str, Any]]:
    missing_example_message = (
        "No example has been added to this event but you can"
        " still explore the event schema. (Ask the developer"
        " to add an example in the event model if you see this"
        " message!)"
    )

    return {
        k: {
            "value": getattr(v, "model_config", {})
            .get("json_schema_extra", {})
            .get("examples", [missing_example_message])[0]
        }
        for k, v in _event_registry().items()
    }


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


@router.post(
    "/",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/cloudevents+json; charset=UTF-8": {
                    "examples": _event_schema_examples(),
                }
            },
        },
    },
    status_code=204,
)
async def submit_event(
    event_data: _EVENTS_UNION_TYPE = Body(
        media_type="application/cloudevents+json; charset=UTF-8",
        discriminator="type",
    ),
    content_type: typing.Literal[
        "application/cloudevents+json; charset=UTF-8"
    ] = Header(),
) -> None:
    pass
