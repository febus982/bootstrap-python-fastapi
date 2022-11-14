import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_root(testapp):
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


@pytest.mark.anyio
async def test_root2(testapp):
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
