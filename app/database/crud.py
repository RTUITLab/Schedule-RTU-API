from sqlalchemy.orm import Session

from . import models, schemas


def get_lessons(db: Session, skip: int = 0, limit: int | None = None, **kwargs):
    kwargs = {
        k: v
        for k, v in kwargs.items()
        if v
    }
    print(kwargs)
    query = db.query(models.Lesson).filter_by(**kwargs).offset(skip).limit(limit).all()
    # print(query)
    # if not limit:
    #     query = db.query(models.Lesson).offset(skip).filter_by(kwargs)
    # else:

    return query
