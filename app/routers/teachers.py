from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db
from .query import TeacherQueryParams

router = APIRouter(
    prefix="/teachers",
    tags=["Преподаватели"]
)


@router.get('/', summary="Получение списка преподавателей",
            response_model=List[schemas.TeacherOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db), queries: TeacherQueryParams = Depends(TeacherQueryParams)):
    return crud.get_teachers(db=db, name=queries.name)


@router.get('/{id}/', summary="Получение преподавателя по id",
            response_model=schemas.TeacherOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    item = crud.get_simpe_model(db=db, id=id, model=models.Teacher)
    if item:
        return item[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Teacher not found")