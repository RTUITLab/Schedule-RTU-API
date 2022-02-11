from sqlalchemy.orm import Session

from . import models, schemas


def create_message(db: Session, new_message: schemas.MessageCreate):
    db_message = models.Message(**new_message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return


def get_messages(db: Session):
    return db.query(models.Message).all()


def delete_message_by_id(db: Session, id: int):
    _ = db.query(models.Message).filter(models.Message.id == id).delete()
    db.commit()
    return
