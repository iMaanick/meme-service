import os
from typing import Optional, AsyncGenerator

import aiohttp
from aiohttp import ClientSession
from fastapi import UploadFile, HTTPException

from app.application.models import Meme, MemeUpdate
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
        meme_data: MemeUpdate,
        database: DatabaseGateway,
        uow: UoW,
) -> Optional[int]:
    updated_meme_id = await database.update_meme_by_id(meme_id, meme_data)
    await uow.commit()
    return updated_meme_id


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


async def delete_meme(
        meme_id: int,
        database: DatabaseGateway,
        uow: UoW,
) -> Optional[int]:
    deleted_meme_id = await database.delete_meme_by_id(meme_id)
    await uow.commit()
    return deleted_meme_id
