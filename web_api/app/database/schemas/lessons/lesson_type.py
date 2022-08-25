from pydantic import BaseModel


class LessonTypeBase(BaseModel):
    short_name: str
    name: str


class LessonTypeOut(LessonTypeBase):
    id: int

    class Config:
        orm_mode = True
