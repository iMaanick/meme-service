from fastapi import FastAPI

from .di import init_dependencies, init_private_dependencies
from .routers import init_routers, init_private_router


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_dependencies(app)
    return app


def create_private_app() -> FastAPI:
    app = FastAPI(title="Private Meme Service")
    init_private_router(app)
    init_private_dependencies(app)
    return app
