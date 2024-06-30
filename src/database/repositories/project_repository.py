from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database import models
from src.database.models import Project
from src.database.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository):
    async def save(self, id: int) -> Project:
        async with self.db_session_manager.session_scope() as session:
            project = Project(id=id)
            session.add(project)
            await session.commit()
            return project

    async def get_project(self, id) -> None or Project:
        async with self.db_session_manager.session_scope() as session:
            query = select(Project).filter_by(id=id)
            result = await session.execute(query)
            db_project = result.scalars().first()
            if db_project:
                return db_project
            else:
                return None

    async def get_project_images(self, project_id) -> list:
        async with self.db_session_manager.session_scope() as session:
            query = (
                select(models.Image)
                .filter_by(project_id=project_id)
                .options(
                    selectinload(models.Image.versions)  # Загрузка связанных версий изображений
                )
            )
            execution = await session.execute(query)
            images = execution.scalars().all()
            response_images = []
            for image in images:
                original_ver = image.versions[0].url if image.versions else None
                thumb_version = image.versions[1].url if image.versions else None
                big_thumb = image.versions[2].url if image.versions else None
                big_1920 = image.versions[3].url if image.versions else None
                d2500 = image.versions[3].url if image.versions else None
                response_image = {
                    "image_id": image.id,
                    "state": image.state,
                    "project_id": image.project_id,
                    "versions": {
                        "original": original_ver,
                        "thumb": thumb_version,
                        "big_thumb": big_thumb,
                        "big_1920": big_1920
                    }
                }
                response_images.append(response_image)

            return response_images

    def to_dict(self):
        return {
            'db_session_manager': self.db_session_manager
        }
