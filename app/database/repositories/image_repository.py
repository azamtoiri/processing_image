import datetime
from typing import Optional, List

from sqlalchemy import select

from app.database.models.image_model import Image, ImageVersion
from app.database.repositories.base_repository import BaseRepository


class ImageRepository(BaseRepository):
    async def update_image_status(self, image_id, status):
        async with self.db_session_manager.session_scope() as session:
            image = await session.get(Image, image_id)
            if image:
                image.status = status
            await session.commit()

    async def update_image_version(self, image_id, type, url):
        async with self.db_session_manager.session_scope() as session:
            query = select(ImageVersion).filter_by(image_id=image_id)
            execute = await session.execute(query)
            image = execute.scalars().all()
            if not image:
                image = ImageVersion(image_id=image_id, type=type, url=url)
                session.add(image)
                await session.commit()
            image.type = type
            image.url = url
            await session.commit()
