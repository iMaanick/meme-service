from unittest.mock import AsyncMock

from starlette.testclient import TestClient

from app.application.models import Meme


def test_get_memes(client: TestClient, mock_database_gateway: AsyncMock) -> None:
    mock_database_gateway.get_memes.return_value = [
        Meme(id=1, description="Test Meme", image_url="http://example.com/test.jpg", filename="test.jpg"),
        Meme(id=2, description="Test Meme 2", image_url="http://example.com/test2.jpg", filename="test2.jpg"),
    ]

    response = client.get("/memes/?skip=0&limit=10")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "description": "Test Meme", "image_url": "http://example.com/test.jpg"},
        {"id": 2, "description": "Test Meme 2", "image_url": "http://example.com/test2.jpg"},
    ]

    mock_database_gateway.get_memes.assert_called_once_with(0, 10)


def test_get_memes_empty_list(client: TestClient, mock_database_gateway: AsyncMock) -> None:
    mock_database_gateway.get_memes.return_value = []

    response = client.get("/memes/?skip=2&limit=3")

    assert response.status_code == 200
    assert response.json() == []

    mock_database_gateway.get_memes.assert_called_once_with(2, 3)
