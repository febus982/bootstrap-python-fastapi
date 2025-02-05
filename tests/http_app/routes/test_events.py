from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from cloudevents_pydantic.events import CloudEvent
from fastapi.testclient import TestClient

from domains.books import BookService
from domains.books.events import BookCreatedV1


class FakeEvent(CloudEvent):
    type: str = "aa"
    # source: Annotated[URIReference, Field(default="https://example.com")]


async def test_event_schema_returns_data_if_present_in_registry(testapp):
    with patch.dict("http_app.routes.events._EVENT_REGISTRY", {"test_event": FakeEvent}, clear=True):
        ac = TestClient(app=testapp, base_url="http://test")
        response = ac.get("/events/dataschemas/test_event")
    assert response.status_code == 200


async def test_event_schema_returns_404_when_not_present_in_registry(testapp):
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/events/dataschemas/inexisting")
    assert response.status_code == 404


async def test_event_schema_list_returns_data_from_registry(testapp):
    with patch.dict("http_app.routes.events._EVENT_REGISTRY", {"test_event": FakeEvent}, clear=True):
        ac = TestClient(app=testapp, base_url="http://test")
        response = ac.get("/events/dataschemas")
    assert response.status_code == 200
    assert response.json() == ["test_event"]


@pytest.mark.parametrize(
    ["batch"],
    (
        pytest.param(True, id="batch"),
        pytest.param(False, id="single"),
    ),
)
async def test_event_endpoints_returns_204(testapp, batch):
    url = "/events" if not batch else "/events/batch"
    content_type = (
        "application/cloudevents+json; charset=UTF-8"
        if not batch
        else "application/cloudevents-batch+json; charset=UTF-8"
    )

    fake_event = BookCreatedV1.event_factory(
        data={"book_id": 0, "title": "string", "author_name": "string"},
    )
    svc = MagicMock(autospec=BookService)
    svc.book_created_event_handler = AsyncMock(return_value=None)
    with patch("domains.books.BookService.__new__", return_value=svc):
        ac = TestClient(app=testapp, base_url="http://test")
        response = ac.post(
            url,
            headers={"content-type": content_type},
            content=fake_event.model_dump_json() if not batch else f"[{fake_event.model_dump_json()}]",
        )
    svc.book_created_event_handler.assert_called_once()
    assert response.status_code == 204


@pytest.mark.parametrize(
    ["batch"],
    (
        pytest.param(True, id="batch"),
        pytest.param(False, id="single"),
    ),
)
async def test_malformed_event_returns_422(testapp, batch):
    url = "/events" if not batch else "/events/batch"
    content_type = (
        "application/cloudevents+json; charset=UTF-8"
        if not batch
        else "application/cloudevents-batch+json; charset=UTF-8"
    )

    class MalformedBookCreatedV1(BookCreatedV1):
        source: Any = None

    fake_event = MalformedBookCreatedV1.event_factory(
        data={"book_id": 0, "title": "string", "author_name": "string"},
    )
    fake_event.source = None
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.post(
        url,
        headers={"content-type": content_type},
        content=fake_event.model_dump_json() if not batch else f"[{fake_event.model_dump_json()}]",
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    ["batch"],
    (
        pytest.param(True, id="batch"),
        pytest.param(False, id="single"),
    ),
)
async def test_wrong_content_type_returns_422(testapp, batch):
    url = "/events" if not batch else "/events/batch"

    fake_event = BookCreatedV1.event_factory(
        data={"book_id": 0, "title": "string", "author_name": "string"},
    )
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.post(
        url,
        headers={"content-type": "application/json"},
        content=fake_event.model_dump_json() if not batch else f"[{fake_event.model_dump_json()}]",
    )
    assert response.status_code == 422
