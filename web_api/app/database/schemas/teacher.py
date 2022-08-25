from pydantic import BaseModel


class TeacherBase(BaseModel):
    name: str


class TeacherOut(TeacherBase):
    id: int

    class Config:
        orm_mode = True
