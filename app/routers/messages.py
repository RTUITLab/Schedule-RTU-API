from fastapi import APIRouter, Depends
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.get('/', summary="Read list of messages",
            response_model=List[schemas.MessageDB])
async def read_messages(db=Depends(get_db)):
    return crud.get_messages(db=db)


@router.post('/', status_code=201, summary="Create new message")
async def create_message(new_message: schemas.MessageCreate,
                         db=Depends(get_db)):
    return crud.create_message(db=db, new_message=new_message)


@router.delete('/{id}/', status_code=204, summary="Delete message by id")
async def delete_message_by_id(id: int, db=Depends(get_db)):
    return crud.delete_message_by_id(db=db, id=id)
