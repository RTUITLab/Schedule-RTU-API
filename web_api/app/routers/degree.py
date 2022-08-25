from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/degrees",
    tags=["Академические степени"]
)


@router.get('', summary="Получение списка академических степеней",
            response_model=List[schemas.DegreeOut],
            status_code=status.HTTP_200_OK)
async def get_many(db=Depends(get_db)):
    return crud.get_simpe_model(db=db, model=models.Degree)


@router.get('/{id}', summary="Получение академической степени по id",
            response_model=schemas.DegreeOut,
            status_code=status.HTTP_200_OK)
async def get_one(id: int, db=Depends(get_db)):
    degree = crud.get_simpe_model(db=db, id=id, model=models.Degree)
    if degree:
        return degree[0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Degree not found")