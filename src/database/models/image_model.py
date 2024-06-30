from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.orm import relationship

from src.database.models.base_model import ModelBase


class Image(ModelBase):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    state = Column(String(50))
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="images")
    versions = relationship("ImageVersion", back_populates="image")

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'project_id': self.project_id,
            'status': self.state
        }


class ImageVersion(ModelBase):
    __tablename__ = "image_versions"

    version_id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    type = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)

    image = relationship("Image", back_populates="versions")
