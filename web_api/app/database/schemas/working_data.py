from pydantic import BaseModel


class WorkingDataBase(BaseModel):
    name: str
    value: str

    class Config:
        orm_mode = True


class WorkingDataOut(WorkingDataBase):
    id: int
    
    class Config:
        orm_mode = True
