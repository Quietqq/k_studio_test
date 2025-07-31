import uuid

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    token: str


class AudioUpload(BaseModel):
    user_id: uuid.UUID
    token: str


class AudioResponse(BaseModel):
    download_url: str
