from typing import List

from pydantic import BaseModel

from src.routes.images.schemas import ImageInfo


class ProjectCreate(BaseModel):
    assistant_id: int
    source: str
    owner: str
    details: str


class ProjectDetails(BaseModel):
    assistant_id: int
    source: str
    owner: str
    details: str


class ProjectImagesResponse(BaseModel):
    images: List[ImageInfo]
