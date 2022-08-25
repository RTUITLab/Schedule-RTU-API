from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db


router = APIRouter(
    prefix="/calls",
    tags=["Расписание звонков"]
)


@router.get('', summary="Получение списка звонков",
            response_model=List[schemas.CallOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db)):
    return crud.get_simpe_model(db=db, model=models.Call)


@router.get('/{id}', summary="Получение звонка по id",
            response_model=schemas.CallOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    call = crud.get_simpe_model(db=db, id=id, model=models.Call)
    print(call)
    if call:
        return call[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Call not found")