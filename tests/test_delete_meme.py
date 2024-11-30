from unittest.mock import AsyncMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from starlette.testclient import TestClient

from app.application.models import Meme


@pytest.mark.asyncio
async def test_delete_meme_by_id(
        client: TestClient,
        mock_database_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_database_gateway.delete_meme_by_id.return_value = Meme(
        id=1,
        description="Test Meme",
        image_url="http://example.com/test.jpg",
        filename="test.jpg"
    )
    monkeypatch.setattr("app.application.meme.delete_file", AsyncMock())

    response = client.delete("/memes/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "Meme deleted successfully"}

    mock_database_gateway.delete_meme_by_id.assert_called_once_with(1)
    mock_uow.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_meme_not_found(
        client: TestClient,
        mock_database_gateway: AsyncMock,
) -> None:
    mock_database_gateway.delete_meme_by_id.return_value = None

    response = client.delete("/memes/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Meme not found"}
