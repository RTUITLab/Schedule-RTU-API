from fastapi import APIRouter, Depends, status, HTTPException, Header
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db
from .query import LessonQueryParams


router = APIRouter(
    prefix="/lessons",
    tags=["Пары (получение расписания)"]
)


@router.get('/', summary="Получение списка пар (расписания)",
            response_model=List[schemas.LessonOut],
            status_code=status.HTTP_200_OK)
async def get_lessons(db=Depends(get_db),
                      queries: LessonQueryParams = Depends(LessonQueryParams)):
    group = None
    teacher_id = None
    room_id = None
    discipline_id = None
    place_id = None
    if not (queries.limit and queries.limit <= 700 or queries.group_name or queries.teacher_name or queries.room_name or queries.discipline_name):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You should set limit/group/teacher/room/discipline. There are over 24,000 lesson records in the database.")

    if queries.place_id:
        query = crud.get_simpe_model(db=db, model=models.Place)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
        else:
            place_id = query[0].id

    if queries.group_name:
        query = crud.get_groups(db=db, name=queries.group_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        else:
            group = query[0]

    if queries.teacher_name:
        query = crud.get_teachers(db=db, name=queries.teacher_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        else:
            teacher_id = query[0].id

    if queries.room_name:
        query = crud.get_rooms(db=db, name=queries.room_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        else:
            room_id = query[0].id

    if queries.discipline_name:
        query = crud.get_disciplines(db=db, name=queries.discipline_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Discipline not found")
        else:
            discipline_id = query[0].id

    return crud.get_lessons(db=db,
                            limit=queries.limit,
                            skip=queries.skip,
                            group=group,
                            teacher_id=teacher_id,
                            room_id=room_id,
                            discipline_id=discipline_id,
                            specific_week=queries.specific_week,
                            week=queries.week,
                            day_of_week=queries.day_of_week,
                            period_id=queries.period_id,
                            lesson_type_id=queries.lesson_type_id,
                            call_id=queries.call_id,
                            is_usual_place=queries.is_usual_place,
                            place_id=place_id)


@router.get('/{id}/', summary="Получение пары по id",
            response_model=schemas.LessonOut,
            status_code=status.HTTP_200_OK)
async def get_lesson(id: int, db=Depends(get_db)):
    lesson =  crud.get_lessons(db=db, id=id)
    if lesson:
        return lesson

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Lesson not found")


# @router.delete('/{id}/', status_code=204, summary="Delete message by id")
# async def delete_message_by_id(id: int, db=Depends(get_db)):
#     return crud.delete_message_by_id(db=db, id=id)

# @router.get("/gen")
# async def root(db=Depends(get_db)):
#     gen_rooms(db=db)
#     return {"message": "Hello World"}
