from pydantic import BaseModel, ConfigDict


class Meme(BaseModel):
    id: int
    description: str
    image_url: str
    filename: str
    model_config = ConfigDict(from_attributes=True)


class MemeData(BaseModel):
    id: int
    description: str
    image_url: str


class MemeCreate(BaseModel):
    description: str
    image_url: str


class MemeUpdate(BaseModel):
    description: str
    image_url: str


class UpdateMemeResponse(BaseModel):
    detail: str


class DeleteMemeResponse(BaseModel):
    detail: str
