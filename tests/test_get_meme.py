from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient

from app.application.models import Meme


@pytest.mark.asyncio
async def test_get_meme_success(client: TestClient, mock_database_gateway: AsyncMock) -> None:
    mock_database_gateway.get_meme_by_id.return_value = Meme(
        id=1, description="Test Meme", image_url="http://example.com/test.jpg", filename="test.jpg"
    )
    response = client.get("/memes/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "description": "Test Meme",
        "image_url": "http://example.com/test.jpg",
    }


@pytest.mark.asyncio
async def test_get_meme_not_found(client: TestClient, mock_database_gateway: AsyncMock) -> None:
    mock_database_gateway.get_meme_by_id.return_value = None

    response = client.get("/memes/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found for specified meme_id."}
