from enum import Enum
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class ImageState(str, Enum):
    init = "init"
    uploaded = "uploaded"
    processing = "processing"
    done = "done"
    error = "error"


class ImageVersion(BaseModel):
    original: str = None
    thumb: str = (150, 120)
    big_thumb: str = (700, 700)
    big_1920: str = (1920, 1080)
    d2500: str = (2500, 2500)


class ImageInfo(BaseModel):
    image_id: str
    state: ImageState = ImageState.init
    project_id: str
    versions: ImageVersion


class ImageUpload(BaseModel):
    filename: str
    project_id: int
