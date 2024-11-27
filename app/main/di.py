import os
from functools import partial
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.api.depends_stub import Stub
from app.application.protocols.database import UoW, DatabaseGateway


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


def init_dependencies(app: FastAPI) -> None:
    session_maker = create_session_maker()

    app.dependency_overrides[AsyncSession] = partial(new_session, session_maker)
    app.dependency_overrides[DatabaseGateway] = new_gateway
    app.dependency_overrides[UoW] = new_uow
