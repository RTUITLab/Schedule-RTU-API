from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Period(_Base):
    __tablename__ = "period"
    id = Column(Integer, primary_key=True, autoincrement=False)
    short_name = Column(String(8), unique=True, index=True)
    name = Column(String(40), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', back_populates='period')

    def __repr__(self):
        return '<Period %r>' % self.name
