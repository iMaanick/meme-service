from fastapi import FastAPI

from app.api import root_router
from app.api.file import private_router


def init_routers(app: FastAPI) -> None:
    app.include_router(root_router)


def init_private_router(app: FastAPI) -> None:
    app.include_router(private_router)
