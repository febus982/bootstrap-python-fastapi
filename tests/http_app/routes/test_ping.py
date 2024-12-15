from fastapi.testclient import TestClient


async def test_root(testapp):
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
