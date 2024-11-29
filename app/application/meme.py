import os
from typing import Optional, AsyncGenerator

import aiohttp
from aiohttp import ClientSession
from fastapi import UploadFile, HTTPException

from app.application.models import Meme, MemeUpdate
from app.application.models.meme import MemeData
from app.application.protocols.database import DatabaseGateway, UoW


async def create_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    async with aiohttp.ClientSession() as session:
        yield session


async def upload_file(
        file: UploadFile,
        session: ClientSession,
) -> str:
    try:
        form_data = aiohttp.FormData()
        form_data.add_field(
            'file',
            await file.read(),
            filename=file.filename,
            content_type=file.content_type
        )
        base_url = os.getenv("PRIVATE_SERVICE_URL", "http://localhost:8001")
        async with session.post(
                f"{base_url}/files/",
                headers={"accept": "application/json"},
                data=form_data
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status,
                                    detail="Failed to upload file to external service.")

            upload_file_response = await response.json()
            filename = upload_file_response['filename']
            return filename
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(err)}")


async def get_file_url(
        filename: str,
        session: ClientSession,
) -> str:
    try:
        base_url = os.getenv("PRIVATE_SERVICE_URL", "http://localhost:8001")
        async with session.get(
                f"{base_url}/files/file-url/",
                params={"filename": filename}
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status,
                                    detail="Failed to get file url from external service.")

            get_file_url_response = await response.json()
            file_url = get_file_url_response['file_url']
            return file_url
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred while getting url of the file: {str(err)}")


async def add_meme(
        description: str,
        file: UploadFile,
        database: DatabaseGateway,
        session: ClientSession,
) -> Meme:
    filename = await upload_file(file, session)
    image_url = await get_file_url(filename, session)
    meme = await database.add_meme(description, filename, image_url)
    return meme


async def update_meme_by_id(
        meme_id: int,
        description: str,
        file: UploadFile,
        database: DatabaseGateway,
        uow: UoW,
        session: ClientSession,

) -> Optional[MemeData]:

    meme = await database.get_meme_by_id(meme_id)
    if not meme:
        return None
    await delete_file(meme.filename, session)
    filename = await upload_file(file, session)
    image_url = await get_file_url(filename, session)
    updated_meme_id = await database.update_meme_by_id(meme_id, description, image_url, filename)
    await uow.commit()
    if not updated_meme_id:
        return None
    return MemeData(
        id=meme_id,
        description=description,
        image_url=image_url,
    )


async def get_meme_data(
        meme_id: int,
        database: DatabaseGateway,
) -> Optional[Meme]:
    meme = await database.get_meme_by_id(meme_id)
    return meme


async def get_memes_data(
        skip: int,
        limit: int,
        database: DatabaseGateway,
) -> list[Meme]:
    memes = await database.get_memes(skip, limit)
    return memes


async def delete_file(
        filename: str,
        session: ClientSession
) -> None:
    try:
        base_url = os.getenv("PRIVATE_SERVICE_URL", "http://localhost:8001")
        async with session.delete(
                f"{base_url}/files/",
                params={"filename": filename}
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail="Failed to delete file from external service."
                )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the file: {str(err)}"
        )


async def delete_meme(
        meme_id: int,
        database: DatabaseGateway,
        uow: UoW,
        session: ClientSession,
) -> Optional[int]:
    deleted_meme = await database.delete_meme_by_id(meme_id)
    await uow.commit()
    if not deleted_meme:
        return None
    await delete_file(deleted_meme.filename, session)
    return deleted_meme.id
