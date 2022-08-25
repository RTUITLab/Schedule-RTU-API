from fastapi import status, HTTPException

from app.database import crud, models
from app.routers.query import LessonQueryParams


def get_lessons_list(queries: LessonQueryParams ,db):
    group = None
    teacher = None
    room_id = None
    discipline_id = None
    place_id = None

    if queries.place_id:
        query = crud.get_simpe_model(db=db, model=models.Place)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
        else:
            place_id = query[0].id

    if queries.group_name:
        query = crud.get_groups(db=db, name=queries.group_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        else:
            group = query[0]

    if queries.teacher_name:
        query = crud.get_teachers(db=db, name=queries.teacher_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        else:
            teacher = query[0]

    if queries.room_name:
        query = crud.get_rooms(db=db, name=queries.room_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        else:
            room_id = query[0].id

    if queries.discipline_name:
        query = crud.get_disciplines(db=db, name=queries.discipline_name)
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Discipline not found")
        else:
            discipline_id = query[0].id

    return crud.get_lessons(db=db,
                            limit=queries.limit,
                            skip=queries.skip,
                            group=group,
                            teacher=teacher,
                            room_id=room_id,
                            discipline_id=discipline_id,
                            specific_week=queries.specific_week,
                            week=queries.week,
                            day_of_week=queries.day_of_week,
                            period_id=queries.period_id,
                            lesson_type_id=queries.lesson_type_id,
                            call_id=queries.call_id,
                            is_usual_place=queries.is_usual_place,
                            place_id=place_id)
