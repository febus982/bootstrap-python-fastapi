from fastapi import status
from fastapi.testclient import TestClient


async def test_create_book(testapp):
    query = "{books{authorName, title, bookId}}"
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.post(
        "/graphql",
        json=dict(query=query),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "data": {"books": [{"authorName": "Stephen King", "bookId": 123, "title": "The Shining"}]}
    }

    """
    Check new_book_data is a subset of response.json()["book"]
    (response.json()["book"] contains also the generated primary key)
    """
