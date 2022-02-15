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
    place: PlaceOut

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
    subgroup: int | None = None
    day_of_week: int
    week: int
    is_usual_place: bool


class SpecificWeek(BaseModel):
    week: int
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

    @validator('specific_weeks')
    def specific_weeks_to_id(cls, v):
        return [x.week for x in v]

    class Config:
        orm_mode = True

class GroupQuery(BaseModel):
    group_name: str | None = Field(None, description="descr text") 
    teacher_name: str | None = None
    room_name: str | None = None
    discipline_name: str | None = None

    specific_week: int | None = None
    week: int | None = None
    day_of_week: int | None = None

    period_id: int | None = None
    lesson_type_id: int | None = None
    call_id: int | None = None

    is_usual_place: bool | None = None
