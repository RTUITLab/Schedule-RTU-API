from tkinter import N
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from . import models, schemas


def get_lessons(db: Session, skip: int = 0, limit: int | None = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    specific_week = None
    group = None
    if "specific_week" in kwargs:
        specific_week = kwargs.pop("specific_week")
        if specific_week % 2:
            week = 1
        else:
            week = 2
        if not "week" in kwargs:
            kwargs["week"] = week
    if "group" in kwargs:
        group = kwargs.pop("group")

    query = db.query(models.Lesson).filter_by(
        **kwargs)

    if group:
        query = query.join(models.Lesson.groups.and_(
            models.Group.id == group.id))

    # if specific_week:

    #     query = query.join(models.SpecificWeek, or_(models.Lesson.every_week, (models.SpecificWeek.secific_week == specific_week) & (
    #         models.SpecificWeek.lesson_id == models.Lesson.id)))

    query = query.offset(skip).limit(limit).all()
    
    if specific_week:
        res = []
        for less in query:
            if specific_week in less.specific_weeks or less.every_week:
                res.append(less)
        query = res

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
