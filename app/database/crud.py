from sqlalchemy.orm import Session

from . import models, schemas


def get_lessons(db: Session, filters: dict, skip: int = 0, limit: int = 1):
    query = db.query(models.Lesson).offset(skip).limit(limit).all()
    return query

def get_groups(db: Session, filters: dict, skip: int = 0, limit: int = 0):
    if not limit:
        query = db.query(models.Lesson).offset(skip).all()
    else:
        query = db.query(models.Lesson).offset(skip).limit(limit).all()
