from src.database.engine.session_maker import DatabaseSessionManager
from src.database.repositories.image_repository import ImageRepository


class Repositories:
    def __init__(self, database_session_manager: DatabaseSessionManager):
        self._db_manager = database_session_manager
        self._image_repository = ImageRepository(self._db_manager)

    @property
    def image_repository(self):
        return self._image_repository
