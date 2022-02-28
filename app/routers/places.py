from pyexpat import model
from statistics import mode
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/places",
    tags=["Кампусы"]
)


@router.get('/', summary="Получение списка кампусов",
            response_model=List[schemas.PlaceOut],
            status_code=status.HTTP_200_OK)
async def get_places(db=Depends(get_db)):

    return crud.get_simpe_model(db=db, model=models.Place)


@router.get('/{id}/', summary="Получение кампуса по id",
            response_model=schemas.PlaceOut,
            status_code=status.HTTP_200_OK)
async def get_places(id: int, db=Depends(get_db)):
    place = crud.get_simpe_model(db=db, id=id, model=models.Place)
    if place:
        return place

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Place not found")