from unittest.mock import patch

from httpx import AsyncClient

from domains.books.entities.cloudevent_base import BaseEvent


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
