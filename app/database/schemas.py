from email.headerregistry import Group
from pydantic import BaseModel, validator, Field


class CallBase(BaseModel):
    call_num: int
    begin_time: str
    end_time: str


class CallOut(CallBase):
    id: int

    class Config:
        orm_mode = True


class PeriodBase(BaseModel):
    short_name: str
    name: str


class PeriodOut(PeriodBase):
    id: int

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
    name: str


class TeacherOut(TeacherBase):
    id: int

    class Config:
        orm_mode = True


class LessonTypeBase(BaseModel):
    short_name: str
    name: str


class LessonTypeOut(LessonTypeBase):
    id: int

    class Config:
        orm_mode = True


class DisciplineBase(BaseModel):
    name: str


class DisciplineOut(DisciplineBase):
    id: int

    class Config:
        orm_mode = True


class PlaceBase(BaseModel):
    short_name: str
    name: str


class PlaceOut(BaseModel):
    id: int
    short_name: str
    name: str

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str


class RoomOut(RoomBase):
    id: int
    name: str
    place: PlaceOut | None = None

    class Config:
        orm_mode = True


class DegreeBase(BaseModel):
    name: str


class DegreeOut(DegreeBase):
    id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str
    year: int


class GroupOut(GroupBase):
    id: int
    degree: DegreeOut

    class Config:
        orm_mode = True


class WorkingDataBase(BaseModel):
    name: str
    value: str


class WorkingDataOut(WorkingDataBase):
    id: int

    class Config:
        orm_mode = True


class LessonBase(BaseModel):
    day_of_week: int
    week: int
    is_usual_place: bool


class SpecificWeek(BaseModel):
    secific_week: int
    lesson_id: int
    class Config:
        orm_mode = True


class Subgroup(BaseModel):
    subgroup: int
    lesson_id: int
    class Config:
        orm_mode = True

class LessonOut(LessonBase):
    id: int
    call: CallOut
    period: PeriodOut
    teacher: TeacherOut | None = None
    lesson_type: LessonTypeOut | None = None
    discipline: DisciplineOut
    room: RoomOut | None = None
    groups: list[GroupOut]
    specific_weeks: list[SpecificWeek]
    subgroups: list[Subgroup]
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
