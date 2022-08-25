from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class SpecificWeek(_Base):
    __tablename__ = "specific_week"
    secific_week = Column(Integer, primary_key=True, autoincrement=False, unique=False)
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True, unique=False)
    lesson = relationship('Lesson', back_populates='specific_weeks')
    

    def __repr__(self):
        return '<SpecificWeeks %r>' % self.secific_week 
