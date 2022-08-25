from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Discipline(_Base):
    __tablename__ = "discipline"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', back_populates='discipline')

    def __repr__(self):
        return '<Discipline %r>' % self.name
