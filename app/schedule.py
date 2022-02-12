# from connect import connect_to_sqlite
import datetime as dt
from datetime import datetime, date, time
import re
from tkinter import NO

from sqlalchemy import false, true
from app import db
from schedule_parser import models
import csv


offset = dt.timedelta(hours=3)


rings = {
    1: {"begin": '9:00', "end": '10:30'},
    2: {"begin": '10:40', "end": '12:10'},
    3: {"begin": '12:40', "end": '14:10'},
    4: {"begin": '14:20', "end": '15:50'},
    5: {"begin": '16:20', "end": '17:50'},
    6: {"begin": '18:00', "end": '19:30'},
    7: {"begin": '19:40', "end": '21:10'},
    8: {"begin": '18:30', "end": '20:00'},
    9: {"begin": '20:10', "end": '21:40'},
}

time_zone = dt.timezone(offset, name='МСК')


def cur_week(today):
    if today.month < 7:
        first = date(today.year, 2, 9)
    else:
        first = date(today.year, 9, 1)

    today_iso = today.isocalendar()
    first_iso = first.isocalendar()
    week = today_iso[1] - first_iso[1]

    if not (first_iso[2] == 7):
        week += 1
    return max(week, 1)


def return_one_day(today, gr):
    week = cur_week(today)
    result = []
    day_of_week = today.isocalendar()[2]

    day = [{
        "time": {"start": '9:00', "end": '10:30'},
        "lesson": None
    }, {
        "time": {"start": '10:40', "end": '12:10'},
        "lesson": None
    }, {
        "time": {"start": '12:40', "end": '14:10'},
        "lesson": None
    }, {
        "time": {"start": '14:20', "end": '15:50'},
        "lesson": None
    }, {
        "time": {"start": '16:20', "end": '17:50'},
        "lesson": None
    }, {
        "time": {"start": '18:00', "end": '19:30'},
        "lesson": None
    }, {
        "time": {"start": '19:40', "end": '21:10'},
        "lesson": None
    }]

    try:
        group = models.Group.query.filter_by(name=gr.strip()).first()
        if not group:
            return None

        lessons = models.Lesson.query.filter_by(
            group_id=group.id, day_of_week=day_of_week)
        
        for lesson in lessons:
            flag = True
            a = models.LessonOnWeek.query.filter_by(lesson=lesson.id).first()
            if a:
                a = models.LessonOnWeek.query.filter_by(
                week=week, lesson=lesson.id).first()
                if not a:
                    flag = False
            if flag:
                res_lesson = {}
                room = models.Room.query.get(lesson.room_id)
                if room:
                    res_lesson["classRoom"] = room.name
                else:
                    res_lesson["classRoom"] = ""

                t = models.Teacher.query.get(
                        lesson.teacher_id)

                if t:
                    res_lesson["teacher"] = t.name
                else:
                    res_lesson["teacher"] = ""

                res_lesson["name"] = models.Discipline.query.get(
                    lesson.discipline_id).name
                
                typ = models.LessonType.query.get(
                        lesson.lesson_type_id)
                if typ:
                    res_lesson["type"] = typ.name
                else:
                    res_lesson["type"] = ""

                day[lesson.call_id-1]['lesson'] = res_lesson

    except Exception as e:
        print("Error", e)
        return None
    return day


def get_groups_old():
    courses = {
        1: "first", 2: "second", 3: "third", 4: "fourth"
    }
    try:
        res = {"bachelor": {"first": [], "second": [], "third": [], "fourth": []},
               "master": {"first": [], "second": []}
               }
        # cursor = connect_to_sqlite()
        record = models.Group.query.filter(
            models.Group.name.startswith('И')).all()
        m = []
        b = []
        a = []
        m_courses = {}
        b_courses = {}
        max_year = 0
        for group_m in record:
            group = group_m.name
            max_year = max(max_year, int(group[-2]+group[-1]))

        for group_m in record:
            group = group_m.name

            if group[2] == "М":
                course = max_year - int(group[-2]+group[-1]) + 1
                ind = -1
                for i in range(len(res["master"][courses[course]])):
                    if res["master"][courses[course]][i]["name"] == group[:4]:
                        ind = i
                if ind != -1:
                    #res["master"][courses[course]][i]["numbers"].append({"number" : int(group[5:7]), "group": group})
                    res["master"][courses[course]][i]["numbers"].append(group)
                else:
                    #res["master"][courses[course]].append({"name": group[:4], "numbers":[{"number" : int(group[5:7]), "group": group}]})
                    res["master"][courses[course]].append(
                        {"name": group[:4], "numbers": [group]})

            elif group[2] == "Б":
                course = max_year - int(group[-2]+group[-1]) + 1
                ind = -1
                for i in range(len(res["bachelor"][courses[course]])):
                    if res["bachelor"][courses[course]][i]["name"] == group[:4]:
                        ind = i
                if ind != -1:
                    res["bachelor"][courses[course]
                                    ][i]["numbers"].append(group)
                    #res["bachelor"][courses[course]][i]["numbers"].append({"number" : int(group[5:7]), "group": group})
                else:
                    res["bachelor"][courses[course]].append(
                        {"name": group[:4], "numbers": [group]})
                    #res["bachelor"][courses[course]].append({"name": group[:4], "numbers":[{"number" : int(group[5:7]), "group": group}]})

            else:
                a.append(group)
        return res
    except Exception as e:
        print("No database")
        print(e.args)
        return None


def today_sch(group):
    today = datetime.now(tz=time_zone)
    return return_one_day(today, group)


def tomorrow_sch(group):
    today = datetime.now(tz=time_zone) + dt.timedelta(days=1)
    return return_one_day(today, group)


def week_sch(group):
    today = datetime.now(tz=time_zone)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    for i in range(6):
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1)
        day = return_one_day(today, group)
        if day:
            res[days[i]] = day
        else:
            return None
    return res


def next_week_sch(group):
    today = datetime.now(tz=time_zone) + dt.timedelta(days=7)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    for i in range(6):
        today = datetime.now(
            tz=time_zone) + dt.timedelta(days=i-day_of_week+1) + dt.timedelta(days=7)
        day = return_one_day(today, group)
        if day:
            res[days[i]] = day
        else:
            return None
    return res


def full_sched(group):
    today = datetime.now(tz=time_zone)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    res2 = {}

    for i in range(6):
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1)
        day = return_one_day(today, group)
        if day:
            res[days[i]] = day
        else:
            return None
    for i in range(6):
        today = datetime.now(
            tz=time_zone) + dt.timedelta(days=i-day_of_week+1) + dt.timedelta(days=7)
        day = return_one_day(today, group)
        if day:
            res2[days[i]] = day
        else:
            return None
    if cur_week(datetime.now(tz=time_zone)) % 2 == 1:
        return {"first": res, "second": res2}
    return {"first": res2, "second": res}


def get_schedule_by_week(group, week):
    today = datetime.now(tz=time_zone)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    for i in range(6):
        day = return_one_day_by_week(week, i, group)
        if day:
            res[days[i-1]] = day
        else:
            return None
    return res


def get_full_schedule_by_weeks(group, max_weeks):
    schedule = []
    for i in range(1, max_weeks+1):
        schedule.append(get_schedule_by_week(group, i))
    return schedule if len(schedule) > 0 else None


def get_group_degree(group):
    if group[2] == "Б":
        degree = "Бакалавриат"

    elif group[2] == "М":
        degree = "Магистратура"

    elif group[2] == "С":
        degree = "Специалитет"
    else:
        degree = "Бакалавриат"
        print("What is", group)

    return degree


def get_group_year(group):
    today = datetime.now(tz=time_zone)
    offset = 0
    current_year = today.year % 2000
    if today.month > 8 and today.day > 20:
        current_year += 1

    year = 1
    try:
        y = int(group[-2] + group[-1])
        year = current_year - y
    except Exception as e:
        print(group, e)

    return year


def get_sem_schedule_by_week(group, specific_week, week, teacher, room):
    result = []
    week_count = 16
    if room:
        room = room.upper()

    try:
        week_count = int(models.WorkingData.query.filter_by(
            name="week_count").first().value)

    except Exception as err:
        print("week_count ERROR! -> ", err) 

    try:
        if group or teacher or room:

            if group:
                gr = models.Group.query.filter_by(
                name=group.strip().upper()).first()
                if not gr:
                    return 'empty'
                lessons = models.Lesson.query.order_by(models.Lesson.week,
                models.Lesson.day_of_week,
                models.Lesson.call_id).filter_by(group_id=gr.id)
                
                    
            if teacher:
                search = "%{}%".format(teacher)
                t = models.Teacher.query.filter(models.Teacher.name.like(search)).first()
                if not t:
                    return 'empty'
                lessons = models.Lesson.query.order_by(models.Lesson.week,
                models.Lesson.day_of_week,
                models.Lesson.call_id).filter_by(teacher_id=t.id)
                

            if room:
                search = "%{}%".format(room)
                r = models.Room.query.filter(models.Room.name.like(search)).first()
                if not r:
                    return 'empty'
                lessons = models.Lesson.query.order_by(models.Lesson.week,
                models.Lesson.day_of_week,
                models.Lesson.call_id).filter_by(room_id=r.id)
                
        else:
            lessons = models.Lesson.query.order_by(models.Lesson.week,
                models.Lesson.day_of_week,
                models.Lesson.call_id).all()
            
        if not week and specific_week:

            if specific_week and int(specific_week)%2:
                week = 1
            elif specific_week:
                week = 2
            
        if week:  
            lessons = [lesson for lesson in lessons if lesson.week == week]
        
        if group:
            group = models.Group.query.filter_by(
                name=group.strip().upper()).first()
            if not group:
                return 'empty'

            lessons = [lesson for lesson in lessons if lesson.group_id == group.id]
        
        if room:
            search = "%{}%".format(room)
            r = models.Room.query.filter(models.Room.name.like(search)).first()
            if not room:
                return 'empty'

            lessons = [lesson for lesson in lessons if lesson.room_id == room.id]

        if teacher:
            search = "%{}%".format(teacher)
            t = models.Teacher.query.filter(models.Teacher.name.like(search)).first()
            if not teacher:
                return 'empty'

            lessons = [lesson for lesson in lessons if lesson.teacher_id == teacher.id]
        less = []
        
        for lesson in lessons:
            less = {
                "call": {
                    "begin_time": "string",
                    "call_num": 0,
                    "end_time": "string",
                    "id": 0
                },
                "day_of_week": 0,
                "discipline": {
                    "id": 0,
                    "name": "string"
                },
                "group": {
                    "degree": "string",
                    "id": 0,
                    "name": "string",
                    "year": 0
                },
                "is_usual_place": "string",
                "lesson_type": {
                    "id": 0,
                    "name": "string",
                    "short_name": "string"
                },
                "period": {
                    "id": 0,
                    "name": "string",
                    "short_name": "string"
                },
                "room": {
                    "name": "string",
                    "place": {
                        "id": 0,
                        "name": "string",
                        "short_name": "string"
                    }
                },
                "specific_weeks": [
                    0
                ],
                "subgroup": 0,
                "teacher": {
                    "id": 0,
                    "name": "string"
                },
                "week": 0
            }

            flag = True
            
            if specific_week:

                weeks = models.LessonOnWeek.query.filter_by(lesson=lesson.id)
                if weeks:
                    w = [x for x in weeks if x.week == specific_week]
                    if not w:
                        flag = false
            
            if flag:
                group = models.Group.query.get(lesson.group_id)
                call = models.Call.query.get(lesson.call_id)
                less["call"] = {
                    "begin_time": call.begin_time,
                    "call_num": call.call_num,
                    "end_time": call.end_time,
                    "id": call.id
                }
                less["day_of_week"] = lesson.day_of_week
                discipline = models.Discipline.query.get(
                    lesson.discipline_id)
                less["discipline"] = {
                    "id": discipline.id,
                    "name": discipline.name
                }
                degree = models.Degree.query.get(
                    group.degree_id)
                less["group"] = {
                    "degree": degree.name,
                    "id": group.id,
                    "name": group.name,
                    "year": group.year
                }

                period = models.Period.query.get(
                    lesson.period_id)

                less["period"] = {
                    "id": period.id,
                    "name": period.name,
                    "short_name": period.short_name
                }

                l_type = models.LessonType.query.filter_by(
                    id=lesson.lesson_type_id).first()

                less["lesson_type"] = None
                if l_type:
                    less["lesson_type"] = {
                        "id": l_type.id,
                        "name": l_type.name,
                        "short_name": l_type.short_name
                    }
                less["room"] = None
                # room = models.Room.query.filter_by(
                #     id=lesson.room_id).first()
                room = models.Room.query.filter_by(
                    id=lesson.room_id).first()
                if room:
                    r_info = {
                        "id": room.id,
                        "name": room.name,
                        "place": None}
                    place = models.Place.query.filter_by(
                        id=room.place_id).first()
                    if place:
                        r_info = {
                            "id": room.id,
                            "name": room.name,
                            "place": {
                                "id": place.id,
                                "name": place.name,
                                "short_name": place.short_name
                            }}

                    less["room"] = r_info

                teacher = models.Teacher.query.filter_by(
                    id=lesson.teacher_id).first()
                less["teacher"] = None
                if teacher:
                    less["teacher"] = {
                        "id": teacher.id,
                        "name": teacher.name
                    },

                less["is_usual_place"] = lesson.is_usual_place
                specific_weeks = models.LessonOnWeek.query.filter_by(lesson=lesson.id)
                specific_weeks = [int(x.week) for x in specific_weeks]
                less["specific_weeks"] = specific_weeks
                less["subgroup"] = lesson.subgroup
                less["week"] = lesson.week

                result.append(less)
                    
            

    except Exception as e:
        print("Error", e)
        return None
    return result


def get_groups_info(institute=None):
    try:
        res = []
        # cursor = connect_to_sqlite()
        if institute:
            if(institute.upper().strip() == "ИИТ"):
                record = models.Group.query.filter(
                    models.Group.name.startswith('И')).all()
            else:
                return []
        else:
            record = models.Group.query.all()

        for gr in record:
            if gr:
                group = gr.name
            else:
                continue

            year = get_group_year(group)

            degree = get_group_degree(group)

            group_info = {
                "name": group,
                "year": year,
                "degree": degree
            }

            res.append(group_info)

        return res

    except Exception as e:
        print("Error", e)
        return None


def get_rooms_info(place=None):
    try:
        res = []
        if place:
            if place:
                place = models.Place.query.filter_by(
                    name=place.strip().upper()).first()

                record = models.Room.query.filter_by(place_id=place.id).all()
        else:
            record = models.Room.query.all()

        for room in record:
            if room:

                place = models.Place.query.get(
                    room.place_id)

                if place:
                    room_info = {
                        "name": room.name,
                        "place": place.name
                    }
                else:
                    continue

                res.append(room_info)
            else:
                continue
        return res

    except Exception as e:
        print("Error", e)
        return None


def get_lessons_list(week=None, specific_week=None, group=None, teacher=None, room=None, discipline=None):
    res = []
    res = get_sem_schedule_by_week(group=group, specific_week=specific_week, week=week, teacher=teacher, room=room)
    return res
