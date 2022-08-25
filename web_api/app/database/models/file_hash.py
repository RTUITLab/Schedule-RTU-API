from sqlalchemy import Column, Integer, String

from app.database.database import Base as _Base


class FileHash(_Base):
    __tablename__ = "file_hash"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, index=True)

    hash = Column(String(40), nullable=True, default=None)

    def __repr__(self):
        return '<FileHash %r>' % self.name
