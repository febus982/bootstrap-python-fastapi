from fastapi import status
from fastapi.testclient import TestClient


async def test_list_books(testapp):
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.get("/api/books/v1/")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert "books" in body
    assert len(body["books"]) == 1
    assert body["books"][0]["title"] == "The Shining"
    assert body["books"][0]["author_name"] == "Stephen King"
