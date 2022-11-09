import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_root(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


@pytest.mark.anyio
async def test_root2(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
