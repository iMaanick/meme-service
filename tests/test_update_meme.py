import os
from unittest.mock import AsyncMock

from _pytest.monkeypatch import MonkeyPatch
from starlette.testclient import TestClient

from app.application.models import Meme


def test_update_meme_success(
        client: TestClient,
        mock_database_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_database_gateway.get_meme_by_id.return_value = Meme(
        id=1, description="Old Meme", image_url="http://example.com/old.jpg", filename="old.jpg"
    )
    mock_database_gateway.update_meme_by_id.return_value = 1
    monkeypatch.setattr("app.application.meme.upload_file", AsyncMock(return_value="new.jpg"))
    monkeypatch.setattr("app.application.meme.get_file_url", AsyncMock(return_value="http://example.com/new.jpg"))
    monkeypatch.setattr("app.application.meme.delete_file", AsyncMock(return_value=None))

    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_file.jpg"), "rb") as test_file:
        response = client.put(
            "/memes/1",
            params={"description": "Updated Meme"},
            files={"file": ("test_image.jpg", test_file, "image/jpeg")},
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "description": "Updated Meme",
        "image_url": "http://example.com/new.jpg",
    }


def test_update_meme_not_found(
        client: TestClient,
        mock_database_gateway: AsyncMock,
        mock_uow: AsyncMock,
        monkeypatch: MonkeyPatch
) -> None:
    mock_database_gateway.get_meme_by_id.return_value = None
    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_file.jpg"), "rb") as test_file:
        response = client.put(
            "/memes/1",
            params={"description": "Updated Meme"},
            files={"file": ("test_image.jpg", test_file, "image/jpeg")},
        )
    assert response.status_code == 404
