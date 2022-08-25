from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Subgroup(_Base):
    __tablename__ = "subgroup"
    subgroup = Column(Integer, primary_key=True, autoincrement=False, unique=False)
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True, unique=False)
    lesson = relationship('Lesson', back_populates='subgroups')


    def __repr__(self):
        return '<Subgroup %r>' % self.subgroup 
