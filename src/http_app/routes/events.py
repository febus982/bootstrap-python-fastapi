import typing
from typing import Dict, List

from domains.books import BookService
from domains.books.events import BookCreatedV1
from fastapi import APIRouter, Body, Header, HTTPException
from fastapi.openapi.models import Example
from pydantic import BaseModel

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


def _event_schema_examples() -> dict[str, Example]:
    missing_example_message = (
        "No example has been added to this event but you can"
        " still explore the event schema. (Ask the developer"
        " to add an example in the event model if you see this"
        " message!)"
    )

    return {
        k: Example(
            value=getattr(v, "model_config", {})
            .get("json_schema_extra", {})
            .get("examples", [missing_example_message])[0]
        )
        for k, v in _event_registry().items()
    }


@router.get(
    "/dataschemas/{event}",
    description="Returns the schema for a supported event",
    responses={404: {"model": str}},
)
async def event_schema(event: str):
    event_model = _event_registry().get(event)
    if event_model:
        return event_model.model_json_schema(mode="serialization")
    else:
        raise HTTPException(status_code=404, detail="Schema not found")


@router.get(
    "/dataschemas",
    description="""
    Provides the list of supported event types. Each event schema can be retrieved
    from the `/dataschemas/{type}` endpoint. The event schema for `book.created.v1`
    is `/dataschemas/book.created.v1`
    """,
)
async def event_schema_list() -> List[str]:
    return list(_event_registry().keys())


@router.post(
    "",
    status_code=204,
    description="""
    Entrypoint for CloudEvent processing, it supports only single events.
    The list of supported CloudEvents and their schema can be retrieved
    from the /events/dataschemas endpoint.
    """,
)
async def submit_event(
    event_data: _EVENTS_UNION_TYPE = Body(
        media_type="application/cloudevents+json; charset=UTF-8",
        openapi_examples=_event_schema_examples(),
        discriminator="type",
    ),
    content_type: typing.Literal[
        "application/cloudevents+json; charset=UTF-8"
    ] = Header(),
) -> None:
    # Some routing will be necessary when multiple event types will be supported
    await BookService().book_created_event_handler(event_data.data.book_id)
