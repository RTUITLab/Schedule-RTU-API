from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db
from .query import LessonQueryParams


router = APIRouter(
    prefix="/lesson",
    tags=["Lessons"]
)


@router.get('/', summary="Получение списка уроков (расписания) ",
            response_model=List[schemas.LessonOut],
            status_code=status.HTTP_200_OK)
async def read_lessons(db=Depends(get_db),
                       commons: LessonQueryParams = Depends(LessonQueryParams)):
    group = None
    teacher_id = None
    room_id = None
    discipline_id = None
    if commons.group_name:
        query = crud.get_groups(db=db, name=commons.group_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        else:
            group = query[0]

    if commons.teacher_name:
        query = crud.get_teachers(db=db, name=commons.teacher_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        else:
            teacher_id = query[0].id

    if commons.room_name:
        query = crud.get_rooms(db=db, name=commons.room_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        else:
            room_id = query[0].id

    if commons.discipline_name:
        query = crud.get_disciplines(db=db, name=commons.discipline_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Discipline not found")
        else:
            discipline_id = query[0].id

    return crud.get_lessons(db=db,
                            group=group,
                            teacher_id=teacher_id,
                            room_id=room_id,
                            discipline_id=discipline_id,
                            specific_week=commons.specific_week,
                            week=commons.week,
                            day_of_week=commons.day_of_week,
                            period_id=commons.period_id,
                            lesson_type_id=commons.lesson_type_id,
                            call_id=commons.call_id,
                            is_usual_place=commons.is_usual_place)


# @router.post('/', status_code=201, summary="Create new message")
# async def create_message(new_message: schemas.MessageCreate,
#                          db=Depends(get_db)):
#     return crud.create_message(db=db, new_message=new_message)


# @router.delete('/{id}/', status_code=204, summary="Delete message by id")
# async def delete_message_by_id(id: int, db=Depends(get_db)):
#     return crud.delete_message_by_id(db=db, id=id)
