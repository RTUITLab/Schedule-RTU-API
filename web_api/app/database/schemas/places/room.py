from pydantic import BaseModel
from typing import Optional
from .place import PlaceOut


class RoomBase(BaseModel):
    name: str


class RoomOut(RoomBase):
    id: int
    name: str
    place: Optional[PlaceOut] = None

    class Config:
        orm_mode = True