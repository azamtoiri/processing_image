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

    # async def save(self,
    #                assistant: str,
    #                name: str,
    #                assistant_prompt: str,
    #                user_prompt: str,
    #                user_prompt_for_chunks: str,
    #                created_at: datetime, ) -> AIAssistant:
    #     async with self.db_session_manager.session_scope() as session:
    #         ai_assistant = AIAssistantModel(
    #             assistant=assistant,
    #             name=name,
    #             assistant_prompt=assistant_prompt,
    #             user_prompt=user_prompt,
    #             user_prompt_for_chunks=user_prompt_for_chunks,
    #             created_at=created_at
    #         )
    #         session.add(ai_assistant)
    #         await session.commit()
    #         return AIAssistant(
    #             assistant=assistant,
    #             name=name,
    #             assistant_prompt=assistant_prompt,
    #             user_prompt=user_prompt,
    #             user_prompt_for_chunks=user_prompt_for_chunks,
    #             created_at=created_at,
    #             assistant_id=ai_assistant.assistant_id
    #         )
    #
    # async def get(self, assistant_id: int) -> Optional[AIAssistant]:
    #     async with self.db_session_manager.session_scope() as session:
    #         query = select(AIAssistantModel).where(AIAssistantModel.assistant_id == assistant_id)
    #         results = await session.execute(query)
    #         result = results.scalars().first()
    #         if result:
    #             return AIAssistant(
    #                 assistant=result.assistant,
    #                 name=result.name,
    #                 assistant_prompt=result.assistant_prompt,
    #                 user_prompt=result.user_prompt,
    #                 user_prompt_for_chunks=result.user_prompt_for_chunks,
    #                 created_at=result.created_at,
    #                 assistant_id=result.assistant_id
    #             )
    #         return None
    #
    # async def get_all(self) -> List[AIAssistant]:
    #     async with self.db_session_manager.session_scope() as session:
    #         query = select(AIAssistantModel)
    #         results = await session.execute(query)
    #         all_results = results.scalars().all()
    #         return [
    #             AIAssistant(
    #                 assistant=result.assistant,
    #                 name=result.name,
    #                 assistant_prompt=result.assistant_prompt,
    #                 user_prompt=result.user_prompt,
    #                 user_prompt_for_chunks=result.user_prompt_for_chunks,
    #                 created_at=result.created_at,
    #                 assistant_id=result.assistant_id
    #             ) for result in all_results
    #         ]
    #
    # # TODO Под вопросом стоит ли передовать объект или так же сделать передачу данных в функцию
    # async def update(self, ai_assistant: AIAssistant) -> bool:
    #     async with self.db_session_manager.session_scope() as session:
    #         entity = await session.get(AIAssistantModel, ai_assistant.assistant_id)
    #         if not entity:
    #             return False
    #         for key, value in ai_assistant.__dict__.items():
    #             setattr(entity, key, value)
    #         await session.commit()
    #         return True
    #
    # async def delete(self, assistant_id: int) -> bool:
    #     async with self.db_session_manager.session_scope() as session:
    #         instance = await session.get(AIAssistantModel, assistant_id)
    #         if instance:
    #             await session.delete(instance)
    #             await session.commit()
    #             return True
    #         return False
