from unittest.mock import patch

from httpx import AsyncClient

from domains.books.events import BookCreatedV1
from domains.common.cloudevent_base import BaseEvent


class FakeEvent(BaseEvent):
    type: str = "aa"


async def test_event_schema_returns_data_if_present_in_registry(testapp):
    with patch(
        "http_app.routes.events._event_registry", return_value={"test_event": FakeEvent}
    ):
        async with AsyncClient(app=testapp, base_url="http://test") as ac:
            response = await ac.get("/events/dataschemas/test_event")
    assert response.status_code == 200


async def test_event_schema_returns_404_when_not_present_in_registry(testapp):
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.get("/events/dataschemas/inexisting")
    assert response.status_code == 404


async def test_event_schema_list_returns_data_from_registry(testapp):
    with patch(
        "http_app.routes.events._event_registry", return_value={"test_event": FakeEvent}
    ):
        async with AsyncClient(app=testapp, base_url="http://test") as ac:
            response = await ac.get("/events/dataschemas")
    assert response.status_code == 200
    assert response.json() == ["test_event"]


async def test_event_returns_204(testapp):
    fake_event = BookCreatedV1(
        data={"book_id": 0, "title": "string", "author_name": "string"},
    )
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.post(
            "/events",
            headers={"content-type": "application/cloudevents+json; charset=UTF-8"},
            content=fake_event.model_dump_json(),
        )
    assert response.status_code == 204


async def test_malformed_event_returns_422(testapp):
    fake_event = BookCreatedV1(
        data={"book_id": 0, "title": "string", "author_name": "string"},
    )
    fake_event.dataschema = None
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.post(
            "/events",
            headers={"content-type": "application/cloudevents+json; charset=UTF-8"},
            content=fake_event.model_dump_json(),
        )
    assert response.status_code == 422


async def test_wrong_content_type_returns_422(testapp):
    fake_event = BookCreatedV1(
        data={"book_id": 0, "title": "string", "author_name": "string"},
    )
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.post(
            "/events",
            headers={"content-type": "application/json"},
            content=fake_event.model_dump_json(),
        )
    assert response.status_code == 422
