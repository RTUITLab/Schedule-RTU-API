from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class LessonType(_Base):
    __tablename__ = "lesson_type"
    id = Column(Integer, primary_key=True, autoincrement=False)
    short_name = Column(String(3), unique=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', back_populates='lesson_type')

    def __repr__(self):
        return '<Lesson_Type %r>' % self.name
