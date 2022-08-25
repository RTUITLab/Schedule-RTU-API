from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/lesson_types",
    tags=["Типы занятий"]
)


@router.get('', summary="Получение списка типов занятий",
            response_model=List[schemas.LessonTypeOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db)):
    return crud.get_simpe_model(db=db, model=models.LessonType)


@router.get('/{id}', summary="Получение типа занятий по id",
            response_model=schemas.LessonTypeOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    lesson_type = crud.get_simpe_model(db=db, id=id, model=models.LessonType)
    if lesson_type:
        return lesson_type[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Lesson type not found")