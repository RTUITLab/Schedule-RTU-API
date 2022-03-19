from importlib.metadata import requires
from fastapi import APIRouter, Depends, Header, Response, status, BackgroundTasks
from sqlalchemy.ext.declarative import declarative_base
# from typing import List

from ..database import crud, schemas
from ..dependencies import get_db, get_settings
from ..utils.schedule_parser.main import parse_schedule


router = APIRouter(
    prefix="/working_data",
    tags=["WorkingData"]
)

settings = get_settings()


@router.post('/refresh/', summary="Обновить расписание",
            status_code=status.HTTP_200_OK)
async def refresh(background_tasks: BackgroundTasks, db=Depends(get_db), X_Auth_Token: str = Header(None), X_Test: bool = Header(None)):
    if X_Auth_Token == settings.app_secret:
        if X_Test:
            background_tasks.add_task(parse_schedule, db, True)
        else:
            background_tasks.add_task(parse_schedule, db)
        return {"detail": "Parsing started"}
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)
    

@router.post('/', summary="Установить вспомогательные данные (weeks_count)", response_model=schemas.WorkingDataOut,
            status_code=status.HTTP_200_OK)
async def set_weeks_count(working_data: schemas.WorkingDataBase, db=Depends(get_db), X_Auth_Token: str = Header(None)):
    
    if X_Auth_Token == settings.app_secret:
        return crud.set_working_data(db=db, data=working_data)
    else:
        return Response("Wrong token", status_code=status.HTTP_401_UNAUTHORIZED)

# @router.post('/', status_code=201, summary="Create new message")
# async def create_message(new_message: schemas.MessageCreate,
#                          db=Depends(get_db)):
#     return crud.create_message(db=db, new_message=new_message)


# @router.delete('/{id}/', status_code=204, summary="Delete message by id")
# async def delete_message_by_id(id: int, db=Depends(get_db)):
#     return crud.delete_message_by_id(db=db, id=id)
