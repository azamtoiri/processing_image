from enum import Enum
from typing import List

from pydantic import BaseModel


class ImageState(str, Enum):
    init = "init"
    uploaded = "uploaded"
    processing = "processing"
    done = "done"
    error = "error"


class ImageVersion(BaseModel):
    original: str = None
    thumb: str
    big_thumb: str
    big_1920: str
    d2500: str


class ImageInfo(BaseModel):
    image_id: int
    state: ImageState = ImageState.init
    project_id: int
    versions: List[ImageVersion]


class ImageUpload(BaseModel):
    filename: str
    project_id: int
