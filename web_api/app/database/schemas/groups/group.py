from pydantic import BaseModel
from ..degree import DegreeOut


class GroupBase(BaseModel):
    name: str
    year: int


class GroupOut(GroupBase):
    id: int
    degree: DegreeOut

    class Config:
        orm_mode = True