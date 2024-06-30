from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import models
from src.database.engine.session_maker import DatabaseSessionManager
from src.utils.config import Connection
from . import schemas

router = APIRouter()


# Dependency to get DB session
async def get_db():
    db = DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
    async with db.session_scope() as db_session:
        yield db_session


# Получение изображений по проекту
@router.get("/{id}/images")
async def get_project_images(id: int, db: AsyncSession = Depends(get_db)):
    query = (
        select(models.Image)
        .filter_by(project_id=id)
        .options(
            selectinload(models.Image.versions)  # Загрузка связанных версий изображений
        )
    )
    execution = await db.execute(query)
    images = execution.scalars().all()
    if not images:
        raise HTTPException(status_code=404, detail=f'Проекта {id} не существует')

    response_images = []
    for image in images:
        response_image = {
            "image_id": image.id,
            "state": image.status,
            "project_id": image.project_id,
            "versions": image.versions
        }
        response_images.append(response_image)

    return {"images": response_images}
