import os
from unittest.mock import AsyncMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from starlette.testclient import TestClient

from app.application.models import Meme


@pytest.mark.asyncio
async def test_create_meme_success(client: TestClient, mock_database_gateway: AsyncMock,
                                   monkeypatch: MonkeyPatch) -> None:
    mock_database_gateway.add_meme.return_value = Meme(
        id=1, description="Test Meme", image_url="http://example.com/test.jpg", filename="test.jpg"
    )

    monkeypatch.setattr("app.application.meme.upload_file", AsyncMock(return_value="test.jpg"))
    monkeypatch.setattr("app.application.meme.get_file_url", AsyncMock(return_value="http://example.com/test.jpg"))

    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_file.jpg"), "rb") as test_file:
        response = client.post(
            "/memes/",
            params={
                "description": "Test Meme",
            },
            files={"file": ("test_image.jpg", test_file, "image/jpeg")},
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "description": "Test Meme",
        "image_url": "http://example.com/test.jpg",
    }


@pytest.mark.asyncio
async def test_create_meme_missing_description(client: TestClient, monkeypatch: MonkeyPatch) -> None:
    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_file.jpg"), "rb") as test_file:
        response = client.post(
            "/memes/",
            files={"file": ("test_image.jpg", test_file, "image/jpeg")},
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"] == ["query", "description"]


@pytest.mark.asyncio
async def test_create_meme_invalid_file_type(client: TestClient) -> None:
    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_invalid.txt"), "rb") as test_file:
        response = client.post(
            "/memes/",
            params={
                "description": "Test Meme",
            },
            files={"file": ("test_invalid.txt", test_file, "text/plain")},
        )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
