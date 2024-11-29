import os
from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_upload_file_success(private_client: TestClient, mock_storage_gateway: AsyncMock):
    mock_storage_gateway.upload_file.return_value = "test_file.jpg"
    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_file.jpg"), "rb") as test_file:
        response = private_client.post(
            "/files/",
            files={"file": ("test_image.jpg", test_file, "image/jpeg")},
        )

    assert response.status_code == 200
    assert response.json() == {
        "detail": "File uploaded successfully",
        "filename": "test_file.jpg",
    }

    mock_storage_gateway.upload_file.assert_called_once()


@pytest.mark.asyncio
async def test_upload_file_invalid_file_type(private_client: TestClient):
    src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))
    with open(os.path.join(src_dir, "test_files/test_invalid.txt"), "rb") as test_file:
        response = private_client.post(
            "/files/",
            files={"file": ("test_invalid.txt", test_file, "text/plain")},
        )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
