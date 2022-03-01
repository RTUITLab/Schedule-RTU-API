from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/groups",
    tags=["Группа"]
)


@router.get('/', summary="Получение списка преподавателей",
            response_model=List[schemas.GroupOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db)):

    return crud.get_simpe_model(db=db, model=models.Group)


@router.get('/{id}/', summary="Получение преподавателя по id",
            response_model=schemas.GroupOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    item = crud.get_simpe_model(db=db, id=id, model=models.Group)
    if item:
        return item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Group not found")