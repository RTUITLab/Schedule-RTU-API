from pydantic import BaseModel


class DisciplineBase(BaseModel):
    name: str


class DisciplineOut(DisciplineBase):
    id: int

    class Config:
        orm_mode = True
