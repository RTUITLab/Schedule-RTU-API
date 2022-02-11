from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from .database import DataBase


class Message(DataBase):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    message = Column(String(), nullable=False)


class Call(DataBase):
    __tablename__ = "call"
    id = Column(Integer, primary_key=True)
    call_num = Column(Integer)
    begin_time = Column(String(16), unique=True, index=True)
    end_time = Column(String(16), unique=True, index=True)

    def __repr__(self):
        return '<Call %r>' % self.name


class Period(DataBase):
    __tablename__ = "period"
    id = Column(Integer, primary_key=True, autoincrement=False)
    short_name = Column(String(8), unique=True, index=True)
    name = Column(String(40), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Period %r>' % self.name


class Teacher(DataBase):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Teacher %r>' % self.name


class LessonType(DataBase):
    __tablename__ = "lesson_type"
    id = Column(Integer, primary_key=True, autoincrement=False)
    short_name = Column(String(3), unique=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Lesson_Type %r>' % self.name


class SpecificWeeks(DataBase):
    __tablename__ = "lesson_on_week"
    week = Column(Integer, primary_key=True, autoincrement=False)
    lesson = Column(Integer, ForeignKey(
        'lesson.id'), nullable=False, primary_key=True)

    def __repr__(self):
        return '<SpecificWeeks %r>' % self.week 


class Discipline(DataBase):
    __tablename__ = "discipline"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Discipline %r>' % self.name


class Place(DataBase):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    short_name = Column(String(8), unique=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Place %r>' % self.name


class Room(DataBase):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=True)

    def __repr__(self):
        return '<Room %r>' % self.name


class Degree(DataBase):
    __tablename__ = "degree"
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Place %r>' % self.name


class Group(DataBase):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String(70), unique=True, nullable=False, index=True)
    year = Column(Integer)
    degree_id = Column(Integer, ForeignKey('degree.id'))

    def __repr__(self):
        return '<Group %r>' % self.name


class WorkingData(DataBase):
    __tablename__ = "working_data"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False, index=True)
    value = Column(String(255), nullable=False, index=True)

    def __repr__(self):
        return '<WorkingData %r>' % self.name


class Lesson(DataBase):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('call.id'), nullable=False)
    period_id = Column(Integer, ForeignKey(
        'period.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey(
        'teacher.id'), nullable=True)
    lesson_type_id = Column(Integer, ForeignKey(
        'lesson_type.id'), nullable=True)
    subgroup = Column(Integer, nullable=True)
    discipline_id = Column(Integer, ForeignKey(
        'discipline.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    day_of_week = Column(Integer, nullable=False)

    week = Column(Integer)

    is_usual_place = Column(Boolean, default=True)

    def __repr__(self):
        return '<Post %r>' % self.id

