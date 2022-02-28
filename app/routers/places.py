from fastapi import APIRouter, Depends, status, HTTPException, Header
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db
from .query import LessonQueryParams


router = APIRouter(
    prefix="/places",
    tags=["Кампусы"]
)


@router.get('/', summary="Получение списка кампусов",
            response_model=List[schemas.LessonOut],
            status_code=status.HTTP_200_OK)
async def get_lessons(db=Depends(get_db),
                      queries: LessonQueryParams = Depends(LessonQueryParams)):

    return crud.get_simpe_model(db=db,)


@router.get('/{id}/', summary="Получение пары по id",
            response_model=schemas.LessonOut,
            status_code=status.HTTP_200_OK)
async def get_lesson(id: int, db=Depends(get_db)):

    if crud.get_lessons(db=db, id=id):
        return crud.get_lessons(db=db, id=id)[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Lesson not found")