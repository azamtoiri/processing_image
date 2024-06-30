from src.database.engine.session_maker import DatabaseSessionManager
from src.database.repositories import ImageRepository, ProjectRepository


class Repositories:
    def __init__(self, database_session_manager: DatabaseSessionManager):
        self._db_manager = database_session_manager
        self._image_repository = ImageRepository(self._db_manager)
        self._project_repository = ProjectRepository(self._db_manager)

    @property
    def image_repository(self):
        return self._image_repository

    @property
    def project_repository(self):
        return self._project_repository
