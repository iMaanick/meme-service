from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.application.file import validate_image_file
from app.application.meme import get_meme_data, get_memes_data, add_meme, update_meme_by_id, delete_meme, create_session
from app.application.models import Meme
from app.application.models.meme import DeleteMemeResponse, UpdateMemeResponse, MemeUpdate
from app.application.protocols.database import DatabaseGateway, UoW

meme_router = APIRouter()


@meme_router.post("/", response_model=Meme)
async def create_meme(
        description: str,
        file: Annotated[UploadFile, Depends(validate_image_file)],
        database: Annotated[DatabaseGateway, Depends()],
) -> Meme:
    """
    Create a new meme.

    Returns:
        Meme: The created meme.
    """
    async for session in create_session():
        meme = await add_meme(description, file, database, session)
        return meme


@meme_router.put("/{meme_id}/", response_model=UpdateMemeResponse)
async def update_meme(
        meme_id: int,
        meme_data: MemeUpdate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> UpdateMemeResponse:
    """
    Update an existing meme by its ID.

    Returns:
        UpdateMemeResponse: Response indicating the update status.

    Raises:
        HTTPException: If the meme is not found.
    """
    updated_meme_id = await update_meme_by_id(meme_id, meme_data, database, uow)
    if not updated_meme_id:
        raise HTTPException(status_code=404, detail="Meme not found")
    return UpdateMemeResponse(detail="Meme updated successfully")


@meme_router.get("/{meme_id}", response_model=Meme)
async def get_meme(
        meme_id: int,
        database: Annotated[DatabaseGateway, Depends()],
) -> Meme:
    """
    Retrieve a specific meme by its ID.

    Returns:
        Meme: The retrieved meme.

    Raises:
        HTTPException: If the meme is not found.
    """
    meme = await get_meme_data(meme_id, database)
    if not meme:
        raise HTTPException(status_code=404, detail="Data not found for specified meme_id.")
    return meme


@meme_router.get("/", response_model=list[Meme])
async def get_memes(
        database: Annotated[DatabaseGateway, Depends()],
        skip: int = 0,
        limit: int = 10,
) -> list[Meme]:
    """
    Retrieve a list of memes with pagination.

    Returns:
        list[Meme]: List of memes.
    """
    # response = await http_client.post("http://localhost:8001/memes/")
    # # response = await http_client.get("http://private_service:8001/memes/")
    # print(response.json())
    memes = await get_memes_data(skip, limit, database)
    return memes


@meme_router.delete("/", response_model=DeleteMemeResponse)
async def delete_meme_by_id(
        meme_id: int,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> DeleteMemeResponse:
    """
    Delete a meme by its ID.

    Returns:
        DeleteMemeResponse: Response indicating whether the meme was successfully deleted.

    Raises:
        HTTPException: If the meme is not found.
    """
    async for session in create_session():
        deleted_meme_id = await delete_meme(meme_id, database, uow, session)
        if not deleted_meme_id:
            raise HTTPException(status_code=404, detail="Meme not found")
        return DeleteMemeResponse(detail="Meme deleted successfully")
