from fastapi import APIRouter, Depends, status, Query
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db


router = APIRouter(
    prefix="/lesson",
    tags=["Lessons"]
)

class CustomQueryParams:
    def __init__(
        self,
        foo: str = Query(..., description="Cool Description for foo"),
        bar: str = Query(..., description="Cool Description for bar"),
    ):
        self.foo = foo
        self.bar = bar


@router.get('/', summary="Read list of lessons",
            response_model=List[schemas.LessonOut], 
            status_code=status.HTTP_200_OK
            )
async def read_lessons(db=Depends(get_db),
                model: schemas.GroupQuery = Depends()):
    print(model.group)
    return crud.get_lessons(db=db)


# @router.post('/', status_code=201, summary="Create new message")
# async def create_message(new_message: schemas.MessageCreate,
#                          db=Depends(get_db)):
#     return crud.create_message(db=db, new_message=new_message)


# @router.delete('/{id}/', status_code=204, summary="Delete message by id")
# async def delete_message_by_id(id: int, db=Depends(get_db)):
#     return crud.delete_message_by_id(db=db, id=id)
