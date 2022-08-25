from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Room(_Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=True)
    lessons = relationship('Lesson', back_populates='room')
    place = relationship('Place', back_populates='rooms')

    def __repr__(self):
        return '<Room %r>' % self.name
