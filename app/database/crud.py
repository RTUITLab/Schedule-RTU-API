from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas


def get_lessons(db: Session, skip: int = 0, limit: int | None = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    print(kwargs)
    if "specific_week" in kwargs:
        specific_week = kwargs.pop("specific_week")
        if specific_week%2:
            week = 1
        else:
            week = 2
        query = db.query(models.Lesson)\
            .filter_by(**kwargs).join(models.SpecificWeek, or_(models.Lesson.every_week, models.SpecificWeek.secific_week==specific_week))\
            .filter(models.Lesson.week==week)\
            .offset(skip).limit(limit).all()
        print(query)

    else:
        query = db.query(models.Lesson).filter_by(
            **kwargs).offset(skip).limit(limit).all()

    return query


def get_groups(db: Session, skip: int = 0, limit: int | None = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    print(kwargs)
    query = db.query(models.Group).filter_by(
        **kwargs).offset(skip).limit(limit).all()

    return query


def get_teachers(db: Session, skip: int = 0, limit: int | None = None, name: str | None = None):
    if name:
        search = "%{}%".format(name.title())
        query = db.query(models.Teacher).filter(
            models.Teacher.name.like(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Teacher).offset(skip).limit(limit).all()
    return query


def get_rooms(db: Session, skip: int = 0, limit: int | None = None, name: str | None = None):
    # TODO need to format name
    if name:
        search = "%{}%".format(name.upper())
        query = db.query(models.Room).filter(
            models.Room.name.like(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Room).offset(skip).limit(limit).all()
    return query


def get_disciplines(db: Session, skip: int = 0, limit: int | None = None, name: str | None = None):
    if name:
        search = "%{}%".format(name.capitalize())
        query = db.query(models.Discipline).filter(
            models.Discipline.name.like(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Discipline).offset(skip).limit(limit).all()
    return query


def get_specific_week(db: Session, **kwargs):
    query = db.query(models.Lesson).filter_by(**kwargs).all()
    return query
