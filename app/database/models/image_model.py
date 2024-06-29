from sqlalchemy import Column, Integer, String, JSON

from app.database.models.base_model import ModelBase


class Image(ModelBase):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    project_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    versions = Column(JSON, nullable=False, default={})

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'project_id': self.project_id,
            'status': self.status
        }
