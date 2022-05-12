from io import BytesIO

import imgkit
import jinja2
from starlette.responses import StreamingResponse

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
        
@app.get("/photo/")
async def photo(teacher : str='',group: str =''):
    try:
        response = requests.get(
            f'https://schedule-rtu.rtuitlab.dev/api/lessons?teacher_name={teacher}&group_name={group}')
    except:
        return Response(content='something went wrong',status_code=500)
    if response.status_code != 200:
        return Response(content='wrong param',status_code=400)

    answer = response.json()
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
        day = week.get(lesson.get('day_of_week'))
        id = lesson.get("call").get("call_num") * 2 - 1 - lesson.get('week') % 2
        elem = next((x for x in day if x.get("id") == id), None)

        if not elem:

            fill_day(day, extra_lesson=True)

            if lesson.get('day_of_week') <= 3:
                fill_day(week.get(lesson.get('day_of_week') + 3), extra_lesson=True)
            else:
                fill_day(week.get(lesson.get('day_of_week') - 3), extra_lesson=True)

            elem = next((x for x in day if x["id"] == id), None)
            img_height += 200

        elem['body'][
            'subject'] += f'{", ".join([str(specific_week) for specific_week in lesson.get("specific_weeks")])} {lesson.get("discipline").get("name")} <br>'

        if len(elem['body']['subject']) > 100:
            elem['body']['font'] = 'subgroups'

        if lesson.get("lesson_type"):
            elem['body']['type'] += f'{lesson.get("lesson_type").get("short_name")}<br>'
        else:
            elem['body']['type'] = ''

        elem['body'][
            'teacher'] += f'{", ".join([teacher_elem.get("name") for teacher_elem in lesson.get("teachers")])}<br>'

        if lesson.get("room"):
            elem['body']['classroom'] += f'{lesson.get("room").get("name")}<br>'
        else:
            elem['body']['classroom'] = ''

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

    payload = {
        'request': f'Расписание преподавателя<br>{teacher}' if teacher else f'Расписание группы<br>{group}',
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
    }, css='./templates/styles.css')
    byte_img = BytesIO(img)

    return StreamingResponse(byte_img, media_type="image/png")
