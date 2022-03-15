from typing import List
from fastapi import APIRouter, Depends, Header, status, Response
# from typing import List

from ..database import crud, schemas, models
from ..dependencies import get_db, get_settings
from ..utils.schedule_parser.main import parse_schedule


router = APIRouter(
    prefix="/files_hashes",
    tags=["WorkingData"]
)

settings = get_settings()


@router.get('/', summary="Посмотреть сохраненные хэши файлов",
            response_model=List[schemas.FileHashOut],
            status_code=status.HTTP_200_OK)
async def read_hashes(db=Depends(get_db), X_Auth_Token: str = Header(None)):
    if X_Auth_Token == settings.app_secret:
        return crud.get_simpe_model(db=db, model=models.FileHash)
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete('/', summary="Почистить хэши файлов для ручного обновления всех файлов",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_hashes(db=Depends(get_db), X_Auth_Token: str = Header(None)):
    if X_Auth_Token == settings.app_secret:
        crud.delete_simpe_model(db=db, model=models.FileHash)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)


# TODO 404?
@router.delete('/{id}/', summary="Почистить хэши файлов для ручного обновления выбранного файла",
               status_code=status.HTTP_204_NO_CONTENT)
async def read_hash(id: int, db=Depends(get_db), X_Auth_Token: str = Header(None)):
    if X_Auth_Token == settings.app_secret:
        crud.delete_simpe_model(db=db, model=models.FileHash, id=id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)
    
