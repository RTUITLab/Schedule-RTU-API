from sqlalchemy.orm import Session

from . import models, schemas
from typing import Optional


def get_lessons(db: Session, skip: int = 0, limit: Optional[int] = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    specific_week = None
    group = None
    teacher = None
    place_id = None
    if "specific_week" in kwargs:
        specific_week = kwargs.pop("specific_week")
        if specific_week % 2:
            week = 1
        else:
            week = 2
        if not "week" in kwargs:
            kwargs["week"] = week
        elif week != kwargs["week"]:
                return []


    if "place_id" in kwargs:
        place_id = kwargs.pop("place_id")

    if "group" in kwargs:
        group = kwargs.pop("group")

    if "teacher" in kwargs:
        teacher = kwargs.pop("teacher")

    query = db.query(models.Lesson).filter_by(
        **kwargs)

    if group:
        query = query.join(models.Lesson.groups.and_(
            models.Group.id == group.id))
    if teacher:
        query = query.join(models.Lesson.teachers.and_(
            models.Teacher.id == teacher.id))

    # if specific_week:

    #     query = query.join(models.SpecificWeek, or_(models.Lesson.every_week, (models.SpecificWeek.secific_week == specific_week) & (
    #         models.SpecificWeek.lesson_id == models.Lesson.id)))

    if place_id:
        query = query.join(models.Room).join(
            models.Place).filter(models.Place.id == place_id)
        # res = []
        # for less in query:
        #     print(less.room)
        #     if less.room and less.room.place and less.room.place.id == place_id:
        #         res.append(less)
        # query = res

    query = query.offset(skip).limit(limit).all()
    
    if specific_week:
        res = []
        for less in query:
            if specific_week in [i.secific_week for i in less.specific_weeks] or less.every_week:
                res.append(less)
        query = res
    if not limit:
        query = query[:600]
    else:
        query = query[skip:limit]
    return query


def get_groups(db: Session, skip: int = 0, limit: Optional[int] = None, name: Optional[str] = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    if name:
        search = "%{}%".format(name)
        query = db.query(models.Group).filter_by(**kwargs).filter(
            models.Group.name.ilike(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Group).filter_by(
            **kwargs).offset(skip).limit(limit).all()
    return query


def get_teachers(db: Session, skip: int = 0, limit: Optional[int] = None, name: Optional[str] = None):
    if name:
        search = "%{}%".format(name)
        query = db.query(models.Teacher).filter(
            models.Teacher.name.ilike(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Teacher).offset(skip).limit(limit).all()
    return query


def get_rooms(db: Session, skip: int = 0, limit: Optional[int] = None, name: Optional[str] = None):
    # TODO need to format name

    if name:
        search = "%{}%".format(name.upper())
        query = db.query(models.Room).filter(
            models.Room.name.ilike(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Room).offset(skip).limit(limit).all()

    return query


def get_disciplines(db: Session, skip: int = 0, limit: Optional[int] = None, name: Optional[str] = None):
    if name:
        search = "%{}%".format(name)
        query = db.query(models.Discipline).filter(
            models.Discipline.name.ilike(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Discipline).offset(skip).limit(limit).all()
    return query


def get_simpe_model(db: Session, model, **kwargs):
    query = db.query(model).filter_by(**kwargs).all()
    return query


def delete_simpe_model(db: Session, model, **kwargs):
    _ = db.query(model).filter_by(**kwargs).delete()
    db.commit()
    return


def set_working_data(db: Session, data: schemas.WorkingDataBase):
    try:
        instance = db.query(models.WorkingData).filter_by(name=data.name).first()
        instance.value = str(data.value)
        db.commit()
        return instance

    except Exception as err:
        instance = models.WorkingData(name=data.name, value=data.value)
        db.add(instance)
        db.commit()
        return instance
