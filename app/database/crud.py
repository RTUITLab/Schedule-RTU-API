from sqlalchemy.orm import Session

from . import models, schemas


def get_lessons(db: Session, skip: int = 0, limit: int | None = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    print(kwargs)
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
        search = "%{}%".format(name)
        query = db.query(models.Teacher).filter(models.Teacher.name.like(search)).offset(skip).limit(limit).all()
    else:
        query = db.query(models.Teacher).offset(skip).limit(limit).all()
    return query
