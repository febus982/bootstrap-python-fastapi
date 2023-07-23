from httpx import AsyncClient


async def test_event_schemas_returns_data_if_present_in_registry(testapp):
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        """
        It's too complex mocking the global _EVENT_REGISTRY because
        of the FastAPI lifecycle. For now we're happy to verify
        it's correct when using one of the existing events.
        """
        response = await ac.get("/events/dataschemas/book.created.v1")
    assert response.status_code == 200


async def test_event_schemas_returns_422_when_not_present_in_registry(testapp):
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        """
        It's too complex mocking the global _EVENT_REGISTRY because
        of the FastAPI lifecycle. For now we're happy to verify
        it fails on an inexisting event, hoping there won't ever
        be an `inexisting` event.
        """
        response = await ac.get("/events/dataschemas/inexisting")
    assert response.status_code == 422
