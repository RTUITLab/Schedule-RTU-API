from pydantic import BaseModel


class PeriodBase(BaseModel):
    short_name: str
    name: str


class PeriodOut(PeriodBase):
    id: int

    class Config:
        orm_mode = True
