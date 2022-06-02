import imgkit
import jinja2

from io import BytesIO
from starlette.responses import StreamingResponse
from fastapi import APIRouter
from fastapi import Response, Depends

from app.routers.query import LessonQueryParams
from app.utils.get_lessons import get_lessons_list
from app.dependencies import get_db

router = APIRouter(
    prefix="/image",
    tags=["Фото"]
)


def fill_day(day, extra_lesson=False):
    week_sign = {
        0: 'I',
        1: 'II',
    }
    if extra_lesson:
        range_start = 12
        range_end = 14

    else:
        range_start = 0
        range_end = 12

    for i in range(range_start, range_end):
        day.append({'id': i,
                    'body': {
                        'lesson_num': f'{i // 2 + 1}',
                        'week': week_sign.get(i % 2),
                        'subject': '',
                        'type': '',
                        'teacher': '',
                        'classroom': '',
                        'font': '',
                    }
                    })


@router.get("/schedule/")
async def photo(queries: LessonQueryParams = Depends(LessonQueryParams), db=Depends(get_db)):
    answer = get_lessons_list(queries=queries, db=db)
    if not answer:
        return Response(content='empty search', status_code=500)

    week = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }
    img_height = 4250

    for k, v in week.items():
        fill_day(v)

    for lesson in answer:
        day = week.get(lesson.day_of_week)
        id = lesson.call.call_num * 2 - 1 - lesson.week % 2
        elem = next((x for x in day if x['id'] == id), None)

        if not elem:

            fill_day(day, extra_lesson=True)

            if lesson.day_of_week <= 3:
                fill_day(week.get(lesson.day_of_week + 3), extra_lesson=True)
            else:
                fill_day(week.get(lesson.day_of_week - 3), extra_lesson=True)

            elem = next((x for x in day if x['id'] == id), None)
            img_height += 200

        elem['body'][
            'subject'] += f'{", ".join([str(specific_week) for specific_week in lesson.specific_weeks])} {lesson.discipline.name} <br>'

        if len(elem['body']['subject']) > 100:
            elem['body']['font'] = 'subgroups'

        if lesson.lesson_type:
            elem['body']['type'] += f'{lesson.lesson_type.short_name}<br>'
        else:
            elem['body']['type'] = ''

        elem['body'][
            'teacher'] += f'{", ".join([teacher_elem.name for teacher_elem in lesson.teachers])}<br>'

        if lesson.room:
            elem['body']['classroom'] += f'{lesson.room.name}<br>'
        else:
            elem['body']['classroom'] = ''

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('app/templates'))

    payload = {
        'request': f'Расписание преподавателя<br>{queries.teacher_name}' if queries.teacher_name else f'Расписание группы<br>{queries.group_name}',
        'monday': week.get(1),
        'tuesday': week.get(2),
        'wednesday': week.get(3),
        'thursday': week.get(4),
        'friday': week.get(5),
        'saturday': week.get(6),
    }
    template = jinja_env.get_template('timetable.html')
    jinja_template = template.render(payload)
    img = imgkit.from_string(jinja_template, False, options={
        'width': 2060,
        'height': img_height,
        "enable-local-file-access": "",
    }, css='app/templates/styles.css')
    byte_img = BytesIO(img)

    return StreamingResponse(byte_img, media_type="image/png")
