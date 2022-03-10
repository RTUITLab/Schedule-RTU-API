from typing import List
from fastapi import APIRouter, Depends, status, Response
# from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db
from ..utils.schedule_parser.main import parse_schedule


router = APIRouter(
    prefix="/files_hashes",
    tags=["WorkingData"]
)


# TODO password
@router.get('/', summary="Посмотреть сохраненные хэши файлов",
            response_model=List[schemas.FileHashOut],
            status_code=status.HTTP_200_OK)
async def read_hashes(db=Depends(get_db)):
    return crud.get_simpe_model(db=db, model=models.FileHash)


# TODO password
@router.delete('/', summary="Почистить хэши файлов для ручного обновления всех файлов независимо от\
     того, обновилось ли расписние на сайте или нет",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_hashes(db=Depends(get_db)):
    crud.delete_simpe_model(db=db, model=models.FileHash)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# TODO password, 404?
@router.delete('/{id}/', summary="Почистить хэши файлов для ручного обновления выбранных файлов независимо\
     от того, обновилось ли расписние на сайте или нет",
               status_code=status.HTTP_204_NO_CONTENT)
async def read_hash(id: int, db=Depends(get_db)):
    crud.delete_simpe_model(db=db, model=models.FileHash, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
