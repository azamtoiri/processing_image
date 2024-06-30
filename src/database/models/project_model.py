from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.database.models.base_model import ModelBase
from src.database.models.image_model import Image


class Project(ModelBase):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    images = relationship("Image", back_populates="project")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.created_at,
        }
