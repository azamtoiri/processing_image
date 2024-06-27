from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    upload_link: str


class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectDetails(BaseModel):
    id: int
    name: str
    description: str
