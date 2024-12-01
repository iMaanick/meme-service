from unittest.mock import AsyncMock

from starlette.testclient import TestClient


def test_delete_file_success(private_client: TestClient, mock_storage_gateway: AsyncMock) -> None:
    mock_storage_gateway.delete_file.return_value = "File 'test_file.jpg' deleted successfully"

    response = private_client.delete("/files/", params={"filename": "test_file.jpg"})
    assert response.status_code == 200
    assert response.json() == {
        "detail": "File 'test_file.jpg' deleted successfully"
    }

    mock_storage_gateway.delete_file.assert_called_once_with("test_file.jpg")


def test_delete_file_not_found(private_client: TestClient, mock_storage_gateway: AsyncMock) -> None:
    mock_storage_gateway.delete_file.return_value = None

    response = private_client.delete("/files/", params={"filename": "nonexistent_file.jpg"})

    assert response.status_code == 404
    assert "File not found" in response.json()["detail"]

    mock_storage_gateway.delete_file.assert_called_once_with("nonexistent_file.jpg")
