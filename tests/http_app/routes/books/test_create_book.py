from fastapi import status
from fastapi.testclient import TestClient


async def test_create_book(testapp):
    new_book_data = dict(
        title="test",
        author_name="another",
    )
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.post(
        "/api/books/v1/",
        json=new_book_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    """
    Check new_book_data is a subset of response.json()["book"]
    (response.json()["book"] contains also the generated primary key)
    """
    assert new_book_data.items() <= response.json()["book"].items()


async def test_create_book_v2(testapp):
    new_book_data = dict(
        title="test",
        author_name="another",
    )
    ac = TestClient(app=testapp, base_url="http://test")
    response = ac.post(
        "/api/books/v2/",
        json=new_book_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    """
    Check new_book_data is a subset of response.json()["book"]
    (response.json()["book"] contains also the generated primary key)
    """
    assert new_book_data.items() <= response.json()["book"].items()
