from pydantic import BaseModel


class DegreeBase(BaseModel):
    name: str


class DegreeOut(DegreeBase):
    id: int

    class Config:
        orm_mode = True
