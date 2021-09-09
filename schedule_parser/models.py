from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db


class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(6), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='call', lazy='dynamic')

    def __repr__(self):
        return '<Call %r>' % self.time


class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(8), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='period', lazy='dynamic')

    def __repr__(self):
        return '<Period %r>' % self.period


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(50), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='teacher', lazy='dynamic')

    def __repr__(self):
        return '<Teacher %r>' % self.teacher_name


class LessonType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_type = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Lesson_Type %r>' % self.lesson_type


class Week(db.Model):
    week_num = db.Column(db.Integer, primary_key=True)
    lessons = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False, primary_key=True)

    def __repr__(self):
        return '<Week %r>' % self.week_num


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='discipline', lazy='dynamic')

    def __repr__(self):
        return '<Discipline %r>' % self.name


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_num = db.Column(db.String(70), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='room', lazy='dynamic')

    def __repr__(self):
        return '<Room %r>' % self.room_num


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_num = db.Column(db.String(70), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Group %r>' % self.group_num


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    call_id = db.Column(db.Integer, db.ForeignKey('call.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    lesson_type_id = db.Column(db.Integer, db.ForeignKey('lesson_type.id'), nullable=False)
    week_id = db.relationship('Week', backref='lesson', lazy='dynamic')
    subgroup_id = db.Column(db.Integer, nullable=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Post %r>' % self.title

    def __repr__(self):
        return '<Room %r>' % self.room_num

