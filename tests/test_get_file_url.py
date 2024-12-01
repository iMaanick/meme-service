from unittest.mock import AsyncMock

from starlette.testclient import TestClient


def test_get_file_url_success(private_client: TestClient, mock_storage_gateway: AsyncMock) -> None:
    mock_storage_gateway.get_file_url.return_value = "http://localhost:9000/test_file.jpg"

    response = private_client.get("/files/file-url/", params={"filename": "test_file.jpg"})

    assert response.status_code == 200
    assert response.json() == {
        "file_url": "http://localhost:9000/test_file.jpg"
    }

    mock_storage_gateway.get_file_url.assert_called_once_with("test_file.jpg")


def test_get_file_url_not_found(private_client: TestClient, mock_storage_gateway: AsyncMock) -> None:
    mock_storage_gateway.get_file_url.return_value = None

    response = private_client.get("/files/file-url/", params={"filename": "nonexistent_file.jpg"})

    assert response.status_code == 404
    assert "File 'nonexistent_file.jpg' not found" in response.json()["detail"]

    mock_storage_gateway.get_file_url.assert_called_once_with("nonexistent_file.jpg")
