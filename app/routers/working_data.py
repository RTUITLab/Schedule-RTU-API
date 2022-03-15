from importlib.metadata import requires
from fastapi import APIRouter, Depends, Header, Response, status, BackgroundTasks
# from typing import List

from ..database import crud, schemas
from ..dependencies import get_db, get_settings
from ..utils.schedule_parser.main import parse_schedule


router = APIRouter(
    prefix="/working_data",
    tags=["WorkingData"]
)

settings = get_settings()


# TODO password
@router.post('/refresh/', summary="Refresh schedule",
            status_code=status.HTTP_200_OK)
async def read_lessons(background_tasks: BackgroundTasks, db=Depends(get_db), X_Auth_Token: str = Header(None)):
    if X_Auth_Token == settings.app_secret:
        background_tasks.add_task(parse_schedule, db)
        return {"detail": "Parsing started"}
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)
    

# TODO password
@router.post('/refresh/', summary="Refresh schedule",
            status_code=status.HTTP_200_OK)
async def read_lessons(background_tasks: BackgroundTasks, db=Depends(get_db), X_Auth_Token: str = Header(None)):
    if X_Auth_Token == settings.app_secret:
        background_tasks.add_task(parse_schedule, db)
        return {"detail": "Parsing started"}
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)

# @router.post('/', status_code=201, summary="Create new message")
# async def create_message(new_message: schemas.MessageCreate,
#                          db=Depends(get_db)):
#     return crud.create_message(db=db, new_message=new_message)


# @router.delete('/{id}/', status_code=204, summary="Delete message by id")
# async def delete_message_by_id(id: int, db=Depends(get_db)):
#     return crud.delete_message_by_id(db=db, id=id)
