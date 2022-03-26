from fastapi import APIRouter, Depends, status, HTTPException, Header
from typing import List

from app.utils.gen_rooms import gen_rooms2

from ..database import crud, schemas, models
from ..dependencies import get_db
from .query import LessonQueryParams


router = APIRouter(
    prefix="/lessons",
    tags=["Пары (получение расписания)"]
)

lesson_example = {
    "day_of_week": 1,
    "week": 1,
    "is_usual_place": None,
    "id": 32,
    "call": {
        "call_num": 1,
        "begin_time": "9:00",
        "end_time": "10:30",
        "id": 1
    },
    "period": {
        "short_name": "semester",
        "name": "Учебный семестр",
        "id": 1
    },
    "teacher": None,
    "lesson_type": {
        "short_name": "лр",
        "name": "Лабораторная работа",
        "id": 3
    },
    "discipline": {
        "name": "Физика",
        "id": 2
    },
    "room": {
        "name": "В-328",
        "id": 4,
        "place": {
            "id": 1,
            "short_name": "В-78",
            "name": "Проспект Вернадского, д.78"
        }
    },
    "groups": [
        {
            "name": "ИКБО-01-21",
            "year": 1,
            "id": 14,
            "degree": {
                "name": "Бакалавриат",
                "id": 1
            }
        }
    ],
    "specific_weeks": [
        3,
        7,
        11,
        15
    ],
    "subgroups": [1],
    "every_week": False
}


@router.get('', summary="Получение списка пар (расписания)",
            response_model=List[schemas.LessonOut],
            description='Одним запросом межет быть возвращено не более 600 пар. Для того, чтобы получить большее \
                        количество используйте несколько запросов с параметрами skip и limit. При работе с OpenAPI и попытке\
                        получения более 200 записей может возникнуть долгая загрузка Response body\
                        для более точного поиска рекомендуется использовать параметры с id вместо name (например discipline_id вместо discipline_name)',
            status_code=status.HTTP_200_OK,
            responses={404: {"detail": "Lesson not found"},
                       200: {
                "description": "Lesson item",
                "content":
                {
                    "application/json": {
                        "example": [lesson_example],
                    }
                },
            }})
async def get_lessons(db=Depends(get_db),
                      queries: LessonQueryParams = Depends(LessonQueryParams)):
    group = None
    teacher = None
    room_id = None
    discipline_id = None
    place_id = None

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
            teacher = query[0]

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
                            teacher=teacher,
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


@router.get('/{id}', summary="Получение пары по id",
            response_model=schemas.LessonOut,
            responses={404: {"detail": "Lesson not found"},
                       200: {
                "description": "Lesson item",
                "content":
                {
                    "application/json": {
                        "example": lesson_example,
                    }
                },
            }}
            )
async def get_lesson(id: int, db=Depends(get_db)):
    lesson = crud.get_lessons(db=db, id=id)
    if lesson:
        return lesson[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Lesson not found")


# @router.delete('/{id}', status_code=204, summary="Delete message by id")
# async def delete_message_by_id(id: int, db=Depends(get_db)):
#     return crud.delete_message_by_id(db=db, id=id)

@router.get("/gen")
async def root(db=Depends(get_db)):
    gen_rooms2(db=db)
    return {"message": "Hello World"}
