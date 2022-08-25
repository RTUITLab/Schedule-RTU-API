from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db


router = APIRouter(
    prefix="/rooms",
    tags=["Аудитории"]
)

@router.get('', summary="Получение списка аудитоий",
            response_model=List[schemas.RoomOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db)):
    return crud.get_simpe_model(db=db, model=models.Room)


@router.get('/{id}', summary="Получение аудитоии по id",
            response_model=schemas.RoomOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    room = crud.get_simpe_model(db=db, id=id, model=models.Room)
    if room:
        return room[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Room not found")