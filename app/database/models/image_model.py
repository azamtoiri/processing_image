from sqlalchemy import Column, Integer, String, JSON

from app.database.models.base_model import ModelBase


class ImageModel(ModelBase):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    project_id = Column(Integer, index=True)
    status = Column(String, default="uploaded")
    versions = Column(JSON, default={})

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'project_id': self.project_id,
            'status': self.status
        }
