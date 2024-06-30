from pathlib import Path

from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates_file_path = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=f"{templates_file_path}/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
