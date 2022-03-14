from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from .database import DataBase


class Call(DataBase):
    __tablename__ = "call"
    id = Column(Integer, primary_key=True)
    call_num = Column(Integer)
    begin_time = Column(String(16), unique=True, index=True)
    end_time = Column(String(16), unique=True, index=True)
    lessons = relationship('Lesson', back_populates='call')

    def __repr__(self):
        return '<Call %r>' % self.call_num


class Period(DataBase):
    __tablename__ = "period"
    id = Column(Integer, primary_key=True, autoincrement=False)
    short_name = Column(String(8), unique=True, index=True)
    name = Column(String(40), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', back_populates='period')

    def __repr__(self):
        return '<Period %r>' % self.name


class LessonType(DataBase):
    __tablename__ = "lesson_type"
    id = Column(Integer, primary_key=True, autoincrement=False)
    short_name = Column(String(3), unique=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', back_populates='lesson_type')

    def __repr__(self):
        return '<Lesson_Type %r>' % self.name


class SpecificWeek(DataBase):
    __tablename__ = "specific_week"
    secific_week = Column(Integer, primary_key=True, autoincrement=False)
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True)
    lesson = relationship('Lesson', back_populates='specific_weeks')

    def __repr__(self):
        return '<SpecificWeeks %r>' % self.secific_week 


class Subgroup(DataBase):
    __tablename__ = "subgroup"
    subgroup = Column(Integer, primary_key=True, autoincrement=False)
    lesson_id = Column(Integer, ForeignKey('lesson.id'), primary_key=True)
    lesson = relationship('Lesson', back_populates='subgroups')

    def __repr__(self):
        return '<Subgroup %r>' % self.subgroup 


class Discipline(DataBase):
    __tablename__ = "discipline"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', back_populates='discipline')

    def __repr__(self):
        return '<Discipline %r>' % self.name


class Place(DataBase):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    short_name = Column(String(8), unique=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    rooms = relationship('Room', back_populates='place')

    def __repr__(self):
        return '<Place %r>' % self.name


class Room(DataBase):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=True)
    lessons = relationship('Lesson', back_populates='room')
    place = relationship('Place', back_populates='rooms')

    def __repr__(self):
        return '<Room %r>' % self.name


class Degree(DataBase):
    __tablename__ = "degree"
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True, nullable=False, index=True)

    groups = relationship('Group', back_populates='degree')

    def __repr__(self):
        return '<Place %r>' % self.name


lesson_teacher = Table('lesson_teacher', DataBase.metadata,
    Column('lesson_id', ForeignKey('lesson.id'), primary_key=True),
    Column('teacher_id', ForeignKey('teacher.id'), primary_key=True)
)


class Teacher(DataBase):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    lessons = relationship('Lesson', secondary=lesson_teacher, back_populates='teachers')

    def __repr__(self):
        return '<Teacher %r>' % self.name


lesson_group = Table('lesson_group', DataBase.metadata,
    Column('lesson_id', ForeignKey('lesson.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True)
)


class Group(DataBase):
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


class WorkingData(DataBase):
    __tablename__ = "working_data"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False, index=True)
    value = Column(String(255), nullable=False, index=True)

    def __repr__(self):
        return '<WorkingData %r>' % self.name


class Institute(DataBase):
    __tablename__ = "institute"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, index=True)
    short_name = Column(String(8), unique=True, index=True)

    def __repr__(self):
        return '<Institute %r>' % self.name


class FileHash(DataBase):
    __tablename__ = "file_hash"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, index=True)

    hash = Column(String(40), nullable=True, default=None)

    def __repr__(self):
        return '<FileHash %r>' % self.name


class Lesson(DataBase):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('call.id'), nullable=False)
    period_id = Column(Integer, ForeignKey(
        'period.id'), nullable=False)
    lesson_type_id = Column(Integer, ForeignKey(
        'lesson_type.id'), nullable=True)
    discipline_id = Column(Integer, ForeignKey(
        'discipline.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=True)

    day_of_week = Column(Integer, nullable=False)
    week = Column(Integer)
    is_usual_place = Column(Boolean, default=True)

    call = relationship("Call", back_populates="lessons")
    period = relationship("Period", back_populates="lessons")
    teachers = relationship("Teacher",
                    secondary=lesson_teacher,
                    back_populates="lessons")
    lesson_type = relationship("LessonType", back_populates="lessons")
    discipline = relationship("Discipline", back_populates="lessons")
    room = relationship("Room", back_populates="lessons")
    groups = relationship("Group",
                    secondary=lesson_group,
                    back_populates="lessons")
    specific_weeks = relationship("SpecificWeek", back_populates="lesson", cascade="all, delete")
    subgroups = relationship("Subgroup", back_populates="lesson", cascade="all, delete")
    every_week = Column(Boolean, default=True)

    def __repr__(self):
        return '<Lesson %r>' % self.id
