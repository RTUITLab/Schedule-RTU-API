from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


lesson_teacher = Table('lesson_teacher', _Base.metadata,
    Column('lesson_id', ForeignKey('lesson.id'), primary_key=True),
    Column('teacher_id', ForeignKey('teacher.id'), primary_key=True)
)


class Teacher(_Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', secondary=lesson_teacher, back_populates='teachers')

    def __repr__(self):
        return '<Teacher %r>' % self.name
