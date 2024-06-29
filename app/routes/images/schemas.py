from fastapi import UploadFile
from pydantic import BaseModel


class ImageUpload(BaseModel):
    project_id: int
    image: UploadFile


class ImageUploadResponse(BaseModel):
    upload_link: str


class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectDetails(BaseModel):
    id: int
    name: str
    description: str


class Image(BaseModel):
    id: int
    url: str
