from typing import (
    Annotated,
    Dict,
    List,
    Literal,
    Type,
    Union,
    get_args,
    get_origin,
)

from fastapi import APIRouter, Body, Header, HTTPException
from fastapi.openapi.models import Example
from pydantic import Field

from domains.books import BookService
from domains.books.events import BookCreatedV1, BookUpdatedV1

router = APIRouter(prefix="/events")

"""
In a real application these events would be the events the app RECEIVES and
not the ones our application SENDS. This is only an example to illustrate
how to handle different CloudEvent classes in FastAPI"""
_EVENTS_UNION_TYPE = Annotated[Union[BookCreatedV1, BookUpdatedV1], Field(discriminator="type")]


def _parse_event_registry() -> Dict[str, Type[_EVENTS_UNION_TYPE]]:
    annotation, field = get_args(_EVENTS_UNION_TYPE)
    discriminator = field.discriminator
    return {
        get_args(m.model_fields[discriminator].annotation)[0]: m
        for m in get_args(annotation)
        if get_origin(m.model_fields[discriminator].annotation) is Literal
    }


_EVENT_REGISTRY = _parse_event_registry()


def _event_schema_examples(mode: Literal["single", "batch"]) -> dict[str, Example]:
    missing_example_message = (
        "No example has been added to this event but you can"
        " still explore the event schema. (Ask the developer"
        " to add an example in the event model if you see this"
        " message!)"
    )
    examples: Dict[str, Union[dict, str]] = {
        k: getattr(v, "model_config", {}).get("json_schema_extra", {}).get("examples", [missing_example_message])[0]
        for k, v in _EVENT_REGISTRY.items()
    }

    return {k: Example(value=v if (mode == "single" or isinstance(v, str)) else [v]) for k, v in examples.items()}


@router.get(
    "/dataschemas/{event}",
    description="Returns the schema for a supported event",
    responses={404: {"model": str}},
)
async def event_schema(event: str):
    event_model = _EVENT_REGISTRY.get(event)
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
    return list(_EVENT_REGISTRY.keys())


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
    event_data: Annotated[
        _EVENTS_UNION_TYPE,
        Body(
            media_type="application/cloudevents+json; charset=UTF-8",
            openapi_examples=_event_schema_examples(mode="single"),
            discriminator="type",
        ),
    ],
    content_type: Annotated[Literal["application/cloudevents+json; charset=UTF-8"], Header()],
) -> None:
    # Some routing will be necessary when multiple event types will be supported
    await BookService().book_created_event_handler(event_data.data.book_id)


@router.post(
    "/batch",
    status_code=204,
    description="""
    Entrypoint for CloudEvent batch processing.
    The list of supported CloudEvents and their schema can be retrieved
    from the /events/dataschemas endpoint.
    """,
)
async def submit_event_batch(
    event_batch: Annotated[
        List[_EVENTS_UNION_TYPE],
        Body(
            media_type="application/cloudevents-batch+json; charset=UTF-8",
            openapi_examples=_event_schema_examples(mode="batch"),
        ),
    ],
    content_type: Annotated[Literal["application/cloudevents-batch+json; charset=UTF-8"], Header()],
) -> None:
    for event in event_batch:
        await BookService().book_created_event_handler(event.data.book_id)
