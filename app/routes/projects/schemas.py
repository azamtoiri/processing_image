from pydantic import BaseModel


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
