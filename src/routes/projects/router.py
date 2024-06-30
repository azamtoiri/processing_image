from fastapi import APIRouter, HTTPException, Request

from src.database.engine.session_maker import DatabaseSessionManager
from src.routes.images import schemas as image_schema
from src.utils.config import Connection
from . import schemas

router = APIRouter()


# Dependency to get DB session
async def get_db():
    db = DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
    async with db.session_scope() as db_session:
        yield db_session


# Получение изображений по проекту
@router.get("/{project_id}/images")
async def get_project_images(request: Request, project_id: int):
    images = await request.app.repositories.project_repository.get_project_images(project_id=project_id)

    if not images:
        raise HTTPException(status_code=404, detail=f'Проекта {project_id} не существует')

    # Construct the response model
    response = schemas.ProjectImagesResponse(images=[
        schemas.ImageInfo(
            image_id=image["image_id"],
            state=image["state"],
            project_id=image["project_id"],
            versions=[
                image_schema.ImageVersion(
                    original=image.get('versions').get('original'),
                    thumb=image.get('versions').get('original'),
                    big_thumb=image.get('versions').get('original'),
                    big_1920=image.get('versions').get('original'),
                    d2500=image.get('versions').get('original')
                )
            ]
        )
        for image in images
    ])

    return response
