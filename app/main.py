import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import websocket
from app.routes.images.router import router as image_router
from app.routes.projects.router import router as project_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


# Подключаем роуты
app.include_router(image_router, prefix="/images", tags=["images"])
app.include_router(project_router, prefix="/projects", tags=["projects"])
app.include_router(websocket.router)

if __name__ == "__main__":
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8080,
        log_level="debug",
        reload=True
    )
