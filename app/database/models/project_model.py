from sqlalchemy import Column, Integer, String, CHAR

from app.database.models.base_model import ModelBase


class Project(ModelBase):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(CHAR(3), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }
