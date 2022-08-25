from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Place(_Base):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    short_name = Column(String(8), unique=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    rooms = relationship('Room', back_populates='place')

    def __repr__(self):
        return '<Place %r>' % self.name
