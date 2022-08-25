from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base
from ..teacher import lesson_teacher
from ..groups import lesson_group


class Lesson(_Base):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('call.id'), nullable=False)
    period_id = Column(Integer, ForeignKey(
        'period.id'), nullable=False)
    lesson_type_id = Column(Integer, ForeignKey(
        'lesson_type.id'), nullable=True)
    discipline_id = Column(Integer, ForeignKey(
        'discipline.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=True)

    day_of_week = Column(Integer, nullable=False)
    week = Column(Integer)
    is_usual_place = Column(Boolean, default=True)

    call = relationship("Call", back_populates="lessons")
    period = relationship("Period", back_populates="lessons")
    teachers = relationship("Teacher",
                    secondary=lesson_teacher,
                    back_populates="lessons")
    lesson_type = relationship("LessonType", back_populates="lessons")
    discipline = relationship("Discipline", back_populates="lessons")
    room = relationship("Room", back_populates="lessons")
    groups = relationship("Group",
                    secondary=lesson_group,
                    back_populates="lessons")
    specific_weeks = relationship("SpecificWeek", back_populates="lesson", cascade="all, delete")
    subgroups = relationship("Subgroup", back_populates="lesson", cascade="all, delete")
    every_week = Column(Boolean, default=True)

    def __repr__(self):
        return '<Lesson %r>' % self.id
