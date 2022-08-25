from pydantic import BaseModel, validator
from typing import Optional, List

from ..time import CallOut, PeriodOut, SpecificWeek
from ..lessons.lesson_type import LessonTypeOut
from ..lessons.discipline import DisciplineOut
from ..teacher import TeacherOut
from ..places import RoomOut
from ..groups import GroupOut
from ..groups.subgroup import Subgroup


class LessonBase(BaseModel):
    day_of_week: int
    week: int
    is_usual_place: bool


class LessonOut(LessonBase):
    id: int
    call: CallOut
    period: PeriodOut
    teachers: List[TeacherOut] 
    lesson_type: Optional[LessonTypeOut] = None
    discipline: DisciplineOut
    room: Optional[RoomOut] = None
    groups: List[GroupOut]
    specific_weeks: List[SpecificWeek]
    subgroups: List[Subgroup]
    every_week: bool

    class Config:
        schema_extra = {
                "day_of_week": 1,
                "week": 1,
                "is_usual_place": None,
                "id": 1143658,
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
                    "id": 95956
                },
                "room": {
                    "name": "В-328",
                    "id": 35239,
                    "place": {
                        "id": 1,
                        "short_name": "В-78",
                        "name": "Проспект Вернадского, д.78"
                    }
                },
                "groups": [
                    {
                        "name": "КАБО-01-21",
                        "year": 1,
                        "id": 39405,
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

    @validator('specific_weeks')
    def specific_weeks_to_id(cls, v):
        return [x.secific_week for x in v]

    @validator('subgroups')
    def subgroup_to_id(cls, v):
        return [x.subgroup for x in v]

    class Config:
        orm_mode = True
