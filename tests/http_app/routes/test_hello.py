from httpx import AsyncClient


async def test_root(testapp):
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.get("/hello/")
    assert response.status_code == 200
