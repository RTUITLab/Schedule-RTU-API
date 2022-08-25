from pydantic import BaseModel


class SpecificWeek(BaseModel):
    secific_week: int
    lesson_id: int
    class Config:
        orm_mode = True
        