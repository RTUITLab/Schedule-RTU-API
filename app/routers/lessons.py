from fastapi import APIRouter, Depends, status, Query
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db


router = APIRouter(
    prefix="/lesson",
    tags=["Lessons"]
)


class CommonQueryParams:
    def __init__(
        self,
        group_name: str | None = Query(
            None, description="Название группы, расписание которой вы хотите узнать"),
        teacher_name: str | None = Query(
            None, description="Имя преподавателя, расписание которого вы хотите узнать"),
        room_name: str | None = Query(
            None, description="Название аудитории, расписание которой вы хотите узнать"),
        discipline_name: str | None = Query(
            None, description="Название группы, расписание которой вы хотите узнать"),

        specific_week: int | None = Query(
            None, description="Определенная неделя, например 1, 3 или 6"),
        week: int | None = Query(
            None, description="Расписание нечетной недели - 1, расписание нечетной - 2"),
        day_of_week: int | None = Query(
            None, description="Номера дней недели идут по порядку: 1 - понедельник, 2 - вторник и т.д."),

        period_id: int | None = Query(
            None, description="id периода, не изменяется, id интересующего периода можно посмотреть в '/period/'"),
        lesson_type_id: int | None = Query(
            None, description="id типов урока, не изменяется, id интересующего типа урока можно посмотреть в '/lesson_type/'"),
        call_id: int | None = Query(
            None, description="id звонков (номеров пар), не изменяется, id интересующего звонка можно посмотреть в '/call/'"),

        is_usual_place: bool = Query(
            None, description="Cool Description for bar"),
    ):
        self.group_name = group_name
        self.teacher_name = teacher_name
        self.room_name = room_name
        self.discipline_name = discipline_name
        self.specific_week = specific_week
        self.week = week
        self.day_of_week = day_of_week
        self.period_id = period_id
        self.lesson_type_id = lesson_type_id
        self.call_id = call_id
        self.is_usual_place = is_usual_place


@router.get('/', summary="Получение списка уроков (расписания) ",
            response_model=List[schemas.LessonOut],
            status_code=status.HTTP_200_OK
            )
async def read_lessons(db=Depends(get_db),
                       commons: CommonQueryParams = Depends(CommonQueryParams)):

    return crud.get_lessons(db=db,
                            group_name=commons.group_name,
                            teacher_name=commons.teacher_name,
                            room_name=commons.room_name,
                            discipline_name=commons.discipline_name,
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
