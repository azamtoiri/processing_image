from sqlalchemy import select

from src.database.models.image_model import Image, ImageVersion
from src.database.repositories.base_repository import BaseRepository
from src.routes.images import schemas


class ImageRepository(BaseRepository):
    async def save(self, filename: str, project_id: int, state: schemas.ImageState):
        async with self.db_session_manager.session_scope() as session:
            image = Image(filename=filename, project_id=project_id, state=state)
            session.add(image)
            await session.commit()
            return image

    async def get_image_by_project_id(self, project_id: int) -> Image:
        async with self.db_session_manager.session_scope() as session:
            query = select(Image).filter_by(project_id=project_id)
            execution = await session.execute(query)
            response = execution.scalars().first()
            return response

    async def update_image_status(self, image_id, status):
        async with self.db_session_manager.session_scope() as session:
            image = await session.get(Image, image_id)
            if image:
                image.status = status
            await session.commit()

    async def update_image_version(self, image_id, type, url):
        async with self.db_session_manager.session_scope() as session:
            image = ImageVersion(image_id=image_id, type=type, url=url)
            session.add(image)
            await session.commit()

    def to_dict(self):
        return {
            'db_session_manager': self.db_session_manager
        }

    @classmethod
    def from_dict(cls, data):
        return cls(db_session_manager=data['db_session_manager'])
