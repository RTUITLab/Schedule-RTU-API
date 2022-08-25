from sqlalchemy import Column, Integer, String

from app.database.database import Base as _Base


class WorkingData(_Base):
    __tablename__ = "working_data"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False, index=True)
    value = Column(String(255), nullable=False, index=True)

    def __repr__(self):
        return '<WorkingData %r>' % self.name
