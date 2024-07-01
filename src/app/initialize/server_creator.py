from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.app.initialize.lifspan import lifespan
from src.database.repositories.storage_container import Repositories
from src.routes import websocket, main
from src.routes.images.router import router as image_router
from src.routes.projects.router import router as project_router
from src.websocket_manager import router as websocket_router


def create_server(repositories: Optional[Repositories] = None):
    server = FastAPI(lifespan=lifespan,
                     title="PROCESS IMAGE",
                     )
    static_files_path = Path(__file__).resolve().parent.parent.parent
    server.mount("/static", StaticFiles(directory=f'{static_files_path}/static'), name="static")

    server.include_router(image_router, prefix='/images', tags=['images'])
    server.include_router(project_router, prefix='/project', tags=['projects'])
    server.include_router(websocket_router)
    server.include_router(main.router, tags=['main'])
    server.repositories = repositories

    return server
