from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.database.engine.session_maker import DatabaseSessionManager
from app.routes.images import schemas
from app.utils.config import Connection

router = APIRouter()


# Dependency to get DB session
async def get_db():
    async with DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}') as db_session:
        yield db_session


# Получение изображений по проекту
@router.get("/{id}/images", response_model=list[schemas.Image])
async def get_project_images(id: int, db: AsyncSession = Depends(get_db)):
    images = db.query(models.Image).filter(models.Image.project_id == id).all()
    return images
