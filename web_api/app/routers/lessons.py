from fastapi import APIRouter, Depends, status, HTTPException, Header
from typing import List

from app.utils.gen_rooms import gen_rooms2

from ..database import crud, schemas
from ..dependencies import get_db
from .query import LessonQueryParams
from app.utils.get_lessons import get_lessons_list


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
async def get_lessons(queries: LessonQueryParams = Depends(LessonQueryParams), db=Depends(get_db)):
    return get_lessons_list(queries=queries, db=db)


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
