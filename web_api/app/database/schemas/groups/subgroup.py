from pydantic import BaseModel


class Subgroup(BaseModel):
    subgroup: int
    lesson_id: int
    class Config:
        orm_mode = True
