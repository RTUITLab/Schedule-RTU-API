from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


class Degree(_Base):
    __tablename__ = "degree"
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True, nullable=False, index=True)

    groups = relationship('Group', back_populates='degree')

    def __repr__(self):
        return '<Place %r>' % self.name
