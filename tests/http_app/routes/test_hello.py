from fastapi import Depends, FastAPI, status
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

from http_app.routes.auth import decode_jwt


async def _fake_decode_jwt(
    security_scopes=None,
    config=None,
    jwks_client=None,
    token=Depends(HTTPBearer()),
):
    return {"token": token.credentials}


async def test_hello_renders_what_returned_by_decoder(
    testapp: FastAPI,
):
    testapp.dependency_overrides[decode_jwt] = _fake_decode_jwt
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get(
        "/hello/",
        headers={"Authorization": "Bearer some_token"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert '"token": "some_token"' in response.text


async def test_hello_returns_403_without_token(testapp: FastAPI):
    testapp.dependency_overrides[decode_jwt] = _fake_decode_jwt
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/hello/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
