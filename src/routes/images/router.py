import json

import requests
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, UploadFile, Body
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.engine.session_maker import DatabaseSessionManager
from src.database.models import Image, Project
from src.routes.images import schemas
from src.routes.websocket import router as websocket_router
from src.tasks import process_image_task
from src.utils.client import get_s3_client
from src.utils.config import Connection

router = APIRouter()
s3_client = get_s3_client()


# Зависимость для получения асинхронной сессии БД
async def get_db():
    db = DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
    async with db.session_scope() as db_session:
        yield db_session


# Загрузка изображения и инициализация задачи Celery
@router.post("/", response_model=schemas.ImageUpload, status_code=201)
async def upload_image(request: Request, filename: str, project_id: int, db: AsyncSession = Depends(get_db)):
    try:
        response = await s3_client.generate_presigned_post(filename)

        db_project = await db.get(Project, project_id)
        if not db_project:
            # Если проект не существует, создаем новый
            db_project = Project(id=project_id, name=project_id)  # Здесь может быть логика для создания имени проекта
            db.add(db_project)
            await db.commit()
            await db.refresh(db_project)

        # generate url
        url = response['url']
        url = url.split('//')[1]

        # generate params
        params = response.get('fields')
        params['project_id'] = project_id

        return JSONResponse(
            {"upload_link": f"http://localhost:8000/images/upload/{url}", "params": params})
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Initial server error: {err}")


@router.post("/upload/{s3_url}/", status_code=201)
async def upload_image(
        request: Request, s3_url: str, file: UploadFile = UploadFile(...), data=Body(...),
        db: AsyncSession = Depends(get_db)
):
    # Если файл не jpeg или png выводим ошибку
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")

    image_data = await file.read()
    files = {'file': (file.filename, image_data)}
    data_dict = json.loads(data)  # from string to dict
    project_id = data_dict['project_id']  # get project id from params
    try:
        # send image to s3
        http_response = requests.post(f'https://{s3_url}', data=data_dict, files=files)

        # save image to db
        db_image = Image(filename=file.filename, project_id=project_id, status="uploaded")
        db.add(db_image)
        await db.commit()
        await db.refresh(db_image)

        # Запуск задачи Celery для обработки изображения
        result = process_image_task.delay(image_id=db_image.id, image_data=image_data, project_id=project_id)
        return JSONResponse({"process_id": result.id})
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Initial server error: {err}")

router.include_router(websocket_router)
