import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_book(testapp):
    new_book_data = dict(
        title="test",
        author_name="another",
    )
    async with AsyncClient(app=testapp, base_url="http://test") as ac:
        response = await ac.post(
            "/api/books/",
            json=new_book_data,
        )
    assert response.status_code == 200
    """
    Check new_book_data is a subset of response.json()["book"]
    (response.json()["book"] contains also the generated primary key)
    """
    assert new_book_data.items() <= response.json()["book"].items()
