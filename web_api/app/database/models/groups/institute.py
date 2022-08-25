from sqlalchemy import Column, Integer, String

from app.database.database import Base as _Base


class Institute(_Base):
    __tablename__ = "institute"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, index=True)
    short_name = Column(String(8), unique=True, index=True)

    def __repr__(self):
        return '<Institute %r>' % self.name
