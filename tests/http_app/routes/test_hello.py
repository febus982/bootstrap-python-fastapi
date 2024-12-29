from fastapi import status
from fastapi.testclient import TestClient


async def test_hello_no_authentication_server(testapp):
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/hello/")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
