from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database.database import Base as _Base


lesson_group = Table('lesson_group', _Base.metadata,
    Column('lesson_id', ForeignKey('lesson.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True)
)


class Group(_Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String(70), unique=True, nullable=False, index=True)
    year = Column(Integer)
    degree_id = Column(Integer, ForeignKey('degree.id'))

    degree = relationship('Degree', back_populates='groups')
    lessons = relationship("Lesson",
                    secondary=lesson_group,
                    back_populates="groups")

    def __repr__(self):
        return '<Group %r>' % self.name
