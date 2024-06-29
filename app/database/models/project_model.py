from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.database.models.base_model import ModelBase
from app.database.models.image_model import Image


class Project(ModelBase):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    images = relationship("Image", back_populates="project")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }
