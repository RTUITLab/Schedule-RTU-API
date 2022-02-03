from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db


class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    name = db.Column(db.String(6), unique=True, nullable=False, index=True)
    lessons = db.relationship('Lesson', backref='call', lazy='dynamic')

    def __repr__(self):
        return '<Call %r>' % self.name


class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(8), unique=True, nullable=False, index=True)
    lessons = db.relationship('Lesson', backref='period', lazy='dynamic')

    def __repr__(self):
        return '<Period %r>' % self.name


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    lessons = db.relationship('Lesson', backref='teacher', lazy='dynamic')

    def __repr__(self):
        return '<Teacher %r>' % self.name


class LessonType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(20), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Lesson_Type %r>' % self.name


class LessonOnWeek(db.Model):
    week = db.Column(db.Integer, primary_key=True, autoincrement=False)
    lesson = db.Column(db.Integer, db.ForeignKey(
        'lesson.id'), nullable=False, primary_key=True)

    def __repr__(self):
        return '<Week %r>' % self.week 


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    lessons = db.relationship('Lesson', backref='discipline', lazy='dynamic')

    def __repr__(self):
        return '<Discipline %r>' % self.name


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, nullable=False, index=True)

    def __repr__(self):
        return '<Place %r>' % self.name


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False, index=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=True)
    lessons = db.relationship('Lesson', backref='room', lazy='dynamic')

    def __repr__(self):
        return '<Room %r>' % self.name


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False, index=True)
    lessons = db.relationship('Lesson', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Group %r>' % self.name


class WorkingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False, index=True)

    def __repr__(self):
        return '<WorkingData %r>' % self.name


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    call_id = db.Column(db.Integer, db.ForeignKey('call.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey(
        'period.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teacher.id'), nullable=False)
    lesson_type_id = db.Column(db.Integer, db.ForeignKey(
        'lesson_type.id'), nullable=False)
    subgroup = db.Column(db.Integer, nullable=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey(
        'discipline.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)

    week = db.Column(db.Integer)

    week_id = db.relationship(
        'LessonOnWeek', backref='lessons', lazy='dynamic')

    is_usual_location = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Post %r>' % self.id

