from fastapi import APIRouter

from .index import index_router
from .meme import meme_router
root_router = APIRouter()

root_router.include_router(
    meme_router,
    prefix="/memes",
    tags=["memes"]
)
root_router.include_router(
    index_router,
)
