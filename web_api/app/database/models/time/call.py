from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Call(_Base):
    __tablename__ = "call"
    id = Column(Integer, primary_key=True)
    call_num = Column(Integer)
    begin_time = Column(String(16), unique=True, index=True)
    end_time = Column(String(16), unique=True, index=True)
    lessons = relationship('Lesson', back_populates='call')

    def __repr__(self):
        return '<Call %r>' % self.call_num
