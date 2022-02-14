from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str


class MessageCreate(MessageBase):
    pass


class MessageDB(MessageBase):
    id: int

    class Config:
        orm_mode = True


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
    degree: GroupBase

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
    subgroup: int
    day_of_week: int
    week: int
    is_usual_place: bool


class LessonOut(LessonBase):
    id: int
    call: CallOut
    period: PeriodOut
    teacher: TeacherOut | None = None
    lesson_type: LessonTypeOut | None = None
    discipline: DisciplineOut
    room: RoomOut | None = None
    groups: list[GroupOut]
    weeks: list[int]

    class Config:
        orm_mode = True
