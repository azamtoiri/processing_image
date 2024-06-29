import json

import requests
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, UploadFile, Body
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine.session_maker import DatabaseSessionManager
from app.database.models import Image, Project
from app.routes.images import schemas
from app.routes.websocket import router as websocket_router
from app.tasks import process_image_task
from app.utils.client import get_s3_client
from app.utils.config import Connection

router = APIRouter()
s3_client = get_s3_client()


# Зависимость для получения асинхронной сессии БД
async def get_db():
    db = DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
    async with db.session_scope() as db_session:
        yield db_session


# Загрузка изображения и инициализация задачи Celery
@router.post("/", response_model=schemas.ImageUpload, status_code=201)
async def upload_image(filename: str, project_id: int, db: AsyncSession = Depends(get_db)):
    response = await s3_client.generate_presigned_post(filename)

    db_project = await db.get(Project, project_id)
    if not db_project:
        # Если проект не существует, создаем новый
        db_project = Project(id=project_id, name=project_id)  # Здесь может быть логика для создания имени проекта
        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)

    url = response['url']
    url = url.split('//')[1]
    return JSONResponse(
        {"upload_link": f"http://localhost:8000/images/upload/{url}{project_id}", "params": response.get('fields')})


@router.post("/upload/{s3_url}/{project_id}", status_code=201)
async def upload_image(
        s3_url: str, file: UploadFile = UploadFile(...), data=Body(...),
        db: AsyncSession = Depends(get_db), project_id: int = int
):
    image_data = await file.read()
    if file.filename:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")
    try:
        files = {'file': (file.filename, image_data)}
        data_dict = json.loads(data)
        http_response = requests.post(f'https://{s3_url}', data=data_dict, files=files)

    except Exception as err:
        print(err)

    db_image = Image(filename=file.filename, project_id=project_id, status="uploaded")
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)

    # Запуск задачи Celery для обработки изображения
    result = process_image_task.delay(db_image.id, image_data)

    return JSONResponse({"process_id": result.id})


@router.get("/tasks/{task_id}", status_code=200)
async def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


router.include_router(websocket_router)
