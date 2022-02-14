from sqlalchemy.orm import Session

from . import models, schemas


def get_lessons(db: Session, skip: int = 0, limit: int = 1):
    return db.query(models.Lesson).offset(skip).limit(limit).all()

