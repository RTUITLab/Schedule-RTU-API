from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db
from .query import DisciplineQueryParams


router = APIRouter(
    prefix="/disciplines",
    tags=["Дисциплины"]
)


@router.get('', summary="Получение списка дисциплин",
            response_model=List[schemas.DisciplineOut],
            status_code=status.HTTP_200_OK,)
async def get_many(db=Depends(get_db), queries: DisciplineQueryParams = Depends(DisciplineQueryParams)):
    return crud.get_disciplines(db=db, name=queries.name)


@router.get('/{id}', summary="Получение дисциплины по id",
            response_model=schemas.DisciplineOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    period = crud.get_simpe_model(db=db, id=id, model=models.Discipline)
    if period:
        return period[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Room not found")
