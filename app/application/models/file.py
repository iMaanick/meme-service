from pydantic import BaseModel


class UploadFileResponse(BaseModel):
    detail: str
    filename: str


class DeleteFileResponse(BaseModel):
    detail: str


class GetFileUrlResponse(BaseModel):
    file_url: str
