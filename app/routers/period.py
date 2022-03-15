from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/periods",
    tags=["Период проведения занятий"]
)


@router.get('/', summary="Получение списка периодов",
            response_model=List[schemas.PeriodOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db)):
    return crud.get_simpe_model(db=db, model=models.Period)


@router.get('/{id}/', summary="Получение периода по id",
            response_model=schemas.PeriodOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    period = crud.get_simpe_model(db=db, id=id, model=models.Period)
    if period:
        return period[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Period not found")