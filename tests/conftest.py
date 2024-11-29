from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.protocols.database import S3StorageGateway
from app.main.routers import init_private_router


@pytest.fixture
def mock_storage_gateway() -> AsyncMock:
    return AsyncMock(spec=S3StorageGateway)


@pytest.fixture
def private_client(mock_storage_gateway: AsyncMock) -> TestClient:
    app = FastAPI()
    init_private_router(app)
    app.dependency_overrides[S3StorageGateway] = lambda: mock_storage_gateway

    return TestClient(app)
