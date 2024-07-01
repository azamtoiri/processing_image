import json
from pathlib import Path

import requests
from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, Body
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from src.database.engine.session_maker import DatabaseSessionManager
from src.routes.images import schemas
from src.tasks import process_image_task
from src.utils.client import get_s3_client
from src.utils.config import Connection

router = APIRouter()
s3_client = get_s3_client()

templates_file_path = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=f"{templates_file_path}/templates")
print(templates_file_path)


# Зависимость для получения асинхронной сессии БД
async def get_db():
    db = DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
    async with db.session_scope() as db_session:
        yield db_session


@router.get('/')
def image_status(request: Request):
    return templates.TemplateResponse(name='task_status.html', context={"request": request})


@router.post("/", response_model=schemas.ImageUpload, status_code=201)
async def upload_image(request: Request, filename: str, project_id: int):
    try:
        response = await s3_client.generate_presigned_post(filename)

        db_project = await request.app.repositories.project_repository.get_project(id=project_id)
        if not db_project:
            # Если проект не существует, создаем новый
            db_project = await request.app.repositories.project_repository.save(id=project_id)

        # generate url
        url = response['url']
        url = url.split('//')[1]

        # generate params
        params = response.get('fields')
        params['project_id'] = db_project.id

        return JSONResponse(
            {"upload_link": f"http://localhost:8000/images/upload/{url}", "params": params})
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Initial server error: {err}")


@router.post("/upload/{s3_url}/", status_code=201)
async def upload_image(
        request: Request, s3_url: str, file: UploadFile = UploadFile(...), data=Body(...),
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
        db_image = await request.app.repositories.image_repository.save(
            filename=file.filename, project_id=project_id,
            state=schemas.ImageState.uploaded
        )

        # Запуск задачи Celery для обработки изображения
        result = process_image_task.delay(image_id=db_image.id, image_data=image_data, project_id=project_id)
        return JSONResponse({"success": True})
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Initial server error: {err}")


@router.get("/task/{task_id}/")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
