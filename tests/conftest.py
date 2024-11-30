from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.protocols.database import S3StorageGateway, UoW, DatabaseGateway
from app.main.routers import init_private_router, init_routers


@pytest.fixture
def mock_storage_gateway() -> AsyncMock:
    return AsyncMock(spec=S3StorageGateway)


@pytest.fixture
def private_client(mock_storage_gateway: AsyncMock) -> TestClient:
    app = FastAPI()
    init_private_router(app)
    app.dependency_overrides[S3StorageGateway] = lambda: mock_storage_gateway

    return TestClient(app)


@pytest.fixture
def mock_uow() -> UoW:
    uow = AsyncMock()
    uow.commit = AsyncMock()
    uow.flush = AsyncMock()
    return uow


@pytest.fixture
def mock_database_gateway() -> DatabaseGateway:
    mock = AsyncMock(DatabaseGateway)
    return mock


@pytest.fixture
def client(mock_database_gateway: AsyncMock, mock_uow: AsyncMock) -> TestClient:
    app = FastAPI()
    init_routers(app)

    app.dependency_overrides[DatabaseGateway] = lambda: mock_database_gateway
    app.dependency_overrides[UoW] = lambda: mock_uow

    return TestClient(app)
