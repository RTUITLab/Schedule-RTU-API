from pydantic import BaseModel


class FileHashBase(BaseModel):
    name: str
    hash: str

    class Config:
        orm_mode = True


class FileHashOut(FileHashBase):
    id: int
    
    class Config:
        orm_mode = True
