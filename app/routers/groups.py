from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from .query import GroupQueryParams

from ..database import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/groups",
    tags=["Группа"]
)


@router.get('/', summary="Получение списка групп",
            response_model=List[schemas.GroupOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db), queries: GroupQueryParams = Depends(GroupQueryParams)):
    return crud.get_groups(db=db, name=queries.name, year=queries.year, degree_id=queries.degree_id)


@router.get('/{id}/', summary="Получение группы по id",
            response_model=schemas.GroupOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    item = crud.get_simpe_model(db=db, id=id, model=models.Group)
    if item:
        return item[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Group not found")
