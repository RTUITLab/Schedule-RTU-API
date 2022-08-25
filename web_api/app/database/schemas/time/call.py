from pydantic import BaseModel


class CallBase(BaseModel):
    call_num: int
    begin_time: str
    end_time: str


class CallOut(CallBase):
    id: int

    class Config:
        orm_mode = True