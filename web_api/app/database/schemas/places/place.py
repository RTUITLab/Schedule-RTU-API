from pydantic import BaseModel


class PlaceBase(BaseModel):
    short_name: str
    name: str


class PlaceOut(BaseModel):
    id: int
    short_name: str
    name: str

    class Config:
        orm_mode = True
