import os
from functools import partial
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.adapters.minio.gateway import MinioGateway
from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.api.depends_stub import Stub
from app.application.protocols.database import UoW, DatabaseGateway, S3StorageGateway


async def new_gateway(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncGenerator[SqlaGateway, None]:
    yield SqlaGateway(session)


async def new_uow(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncSession:
    return session


def create_session_maker() -> async_sessionmaker[AsyncSession]:
    load_dotenv()
    db_uri = os.getenv('DATABASE_URI')
    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_async_engine(
        db_uri,
        echo=True,
        # pool_size=15,
        # max_overflow=15,
        # connect_args={
        #     "connect_timeout": 5,
        # },
    )
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def new_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


async def get_minio_client() -> AsyncGenerator[MinioGateway, None]:
    yield MinioGateway()


async def get_http_client() -> AsyncClient:
    async with AsyncClient() as client:
        yield client


def init_dependencies(app: FastAPI) -> None:
    session_maker = create_session_maker()

    app.dependency_overrides[AsyncSession] = partial(new_session, session_maker)
    app.dependency_overrides[DatabaseGateway] = new_gateway
    app.dependency_overrides[UoW] = new_uow
    app.dependency_overrides[AsyncClient] = get_http_client


def init_private_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[S3StorageGateway] = get_minio_client
