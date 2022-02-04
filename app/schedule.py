# from connect import connect_to_sqlite
import datetime as dt
from datetime import datetime, date, time
from tkinter import NO
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
            a = models.LessonOnWeek.query.filter_by(
                week=week, lesson=lesson.id).first()
            if a:
                res_lesson = {}

                res_lesson["classRoom"] = models.Room.query.get(
                    lesson.room_id).name
                res_lesson["teacher"] = models.Teacher.query.get(
                    lesson.teacher_id).name
                res_lesson["name"] = models.Discipline.query.get(
                    lesson.discipline_id).name
                res_lesson["type"] = models.LessonType.query.get(
                    lesson.lesson_type_id).name

                day[lesson.call_id-1]['lesson'] = res_lesson

    except Exception as e:
        print("Error", e)
        return None
    return day


def get_groups():
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


def get_sem_schedule(group, week):
    result = [{"day_num": 1,
               "name": "Понедельник",
               "lessons": []},
              {"day_num": 2,
               "name": "Вторник",
               "lessons": []},
              {"day_num": 3,
               "name": "Среда",
               "lessons": []},
              {"day_num": 4,
               "name": "Чертверг",
               "lessons": []},
              {"day_num": 5,
               "name": "Пятница",
               "lessons": []},
              {"day_num": 6,
               "name": "Суббота",
               "lessons": []}]

    try:

        group = models.Group.query.filter_by(
            name=group.strip().upper()).first()
        if not group:
            return None

        for i in range(0, 6):

            lessons = models.Lesson.query.filter_by(
                group_id=group.id, day_of_week=i+1).order_by(models.Lesson.call_id).all()
            less = []

            for lesson in lessons:

                a = models.LessonOnWeek.query.filter_by(
                    week=week, lesson=lesson.id).first()
                if a:
                    room = models.Room.query.get(
                        lesson.room_id)
                    res_lesson = {}

                    res_lesson["callNumber"] = lesson.call_id
                    res_lesson["room"] = room.name
                    res_lesson["specific_weeks"] = [week]

                    res_lesson["teacher"] = models.Teacher.query.get(
                        lesson.teacher_id).name
                    res_lesson["name"] = models.Discipline.query.get(
                        lesson.discipline_id).name
                    res_lesson["type"] = models.LessonType.query.get(
                        lesson.lesson_type_id).name

                    res_lesson["isUsualLocation"] = lesson.is_usual_location

                    if room.place_id:

                        res_lesson["location"] = models.Place.query.get(
                            room.place_id).name
                    else:
                        res_lesson["location"] = ""

                    res_lesson["time"] = rings[lesson.call_id]
                    if res_lesson["isUsualLocation"]:
                        res_lesson["fullRoomName"] = res_lesson["room"]
                    else:
                        res_lesson["fullRoomName"] = res_lesson["location"] + \
                            "* " + res_lesson["room"]
                    less.append(res_lesson)

            result[i]["lessons"] = less

    except Exception as e:
        print("Error", e)
        return None
    return result


def get_full_sem_schedule(group):
    try:
        group = models.Group.query.filter_by(
            name=group.strip().upper()).first()
        if not group:
            return None

        week_count = 16
        try:
            week_count = int(models.WorkingData.query.filter_by(
                name="week_count").first().value)

        except Exception as err:
            print("week_count ERROR! -> ", err)

        result = [{"days": [], "num": 1}, {"days": [], "num": 2}]
        lens = [0, len([i for i in range(1, week_count+1, 2)]),
                len([i for i in range(2, week_count+1, 2)])]

        for j in range(1, 3):
            max_len = lens[j]
            week = [{"day_num": 1,
                    "name": "Понедельник",
                     "lessons": []},
                    {"day_num": 2,
                    "name": "Вторник",
                     "lessons": []},
                    {"day_num": 3,
                    "name": "Среда",
                     "lessons": []},
                    {"day_num": 4,
                    "name": "Чертверг",
                     "lessons": []},
                    {"day_num": 5,
                    "name": "Пятница",
                     "lessons": []},
                    {"day_num": 6,
                    "name": "Суббота",
                     "lessons": []}]

            for i in range(0, 6):

                lessons = models.Lesson.query.filter_by(
                    group_id=group.id, day_of_week=i+1, week=j).order_by(models.Lesson.call_id).all()

                less = []
                for lesson in lessons:
                    weeks = models.LessonOnWeek.query.filter_by(
                        lesson=lesson.id).all()
                    weeks = [w.week for w in weeks]

                    if not len(weeks):
                        result[i]["lessons"] = less
                        continue
                    if len(weeks) == max_len:
                        weeks = []

                    room = models.Room.query.get(
                        lesson.room_id)
                    res_lesson = {}

                    res_lesson["callNumber"] = lesson.call_id
                    res_lesson["specific_weeks "] = weeks

                    res_lesson["room"] = room.name
                    res_lesson["teacher"] = models.Teacher.query.get(
                        lesson.teacher_id).name
                    res_lesson["name"] = models.Discipline.query.get(
                        lesson.discipline_id).name
                    res_lesson["name"] = models.Discipline.query.get(
                        lesson.discipline_id).name
                    res_lesson["type"] = models.LessonType.query.get(
                        lesson.lesson_type_id).name

                    res_lesson["isUsualLocation"] = lesson.is_usual_location

                    if room.place_id:
                        res_lesson["location"] = models.Place.query.get(
                            room.place_id).name
                    else:
                        res_lesson["location"] = ""

                    res_lesson["time"] = rings[lesson.call_id]
                    if res_lesson["isUsualLocation"]:
                        res_lesson["fullRoomName"] = res_lesson["room"]
                    else:
                        res_lesson["fullRoomName"] = res_lesson["location"] + \
                            "* " + res_lesson["room"]
                    less.append(res_lesson)

                week[i]["lessons"] = less

            result[j-1] = week

    except Exception as e:
        print("Error", e)
        return None
    return result


def get_rooms_schedule_by_week(room, week, location):
    result = [{"day_num": 1,
               "name": "Понедельник",
               "lessons": []},
              {"day_num": 2,
               "name": "Вторник",
               "lessons": []},
              {"day_num": 3,
               "name": "Среда",
               "lessons": []},
              {"day_num": 4,
               "name": "Чертверг",
               "lessons": []},
              {"day_num": 5,
               "name": "Пятница",
               "lessons": []},
              {"day_num": 6,
               "name": "Суббота",
               "lessons": []}]
               
    try:
        if location:
            place_id = models.Place.query.filter_by(
                name=location.strip().upper()).first().id

            room = models.Room.query.filter_by(
                name=room.strip().upper(), place_id=place_id).first()
            print(room)
            
        else:
            room = models.Room.query.filter_by(
                name=room.strip().upper()).first()

        if not room:
            return None

        for i in range(0, 6):

            lessons = models.Lesson.query.filter_by(
                day_of_week=i+1, room_id=room.id).order_by(models.Lesson.call_id)
            less = []

            for lesson in lessons:

                a = models.LessonOnWeek.query.filter_by(
                    week=week, lesson=lesson.id).first()
                if a:
                    room = models.Room.query.get(
                        lesson.room_id)
                    res_lesson = {}

                    res_lesson["callNumber"] = lesson.call_id
                    res_lesson["room"] = room.name
                    res_lesson["specific_weeks"] = [week]

                    res_lesson["teacher"] = models.Teacher.query.get(
                        lesson.teacher_id).name
                    res_lesson["name"] = models.Discipline.query.get(
                        lesson.discipline_id).name
                    res_lesson["type"] = models.LessonType.query.get(
                        lesson.lesson_type_id).name

                    res_lesson["isUsualLocation"] = lesson.is_usual_location

                    if room.place_id:

                        res_lesson["location"] = models.Place.query.get(
                            room.place_id).name
                    else:
                        res_lesson["location"] = ""

                    res_lesson["time"] = rings[lesson.call_id]
                    if res_lesson["isUsualLocation"]:
                        res_lesson["fullRoomName"] = res_lesson["room"]
                    else:
                        res_lesson["fullRoomName"] = res_lesson["location"] + \
                            "* " + res_lesson["room"]
                    less.append(res_lesson)

            result[i]["lessons"] = less

    except Exception as e:
        print("Error", e)
        return None

    return result


def get_groups_info(institute=None):
    try:
        today = datetime.now(tz=time_zone)
        offset = 0
        current_year = today.year % 2000
        if today.month > 8 and today.day > 20:
            current_year += 1

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
                
            year = 1
            try:
                y = int(group[-2] + group[-1])
                year = current_year - y
            except Exception as e:
                print(group, e)

            if group[2] == "Б":
                degree = "Бакалавриат"

            elif group[2] == "М":
                degree = "Магистратура"

            elif group[2] == "С":
                degree = "Специалитет"
            else:
                degree = "Бакалавриат"
                print("What is", group)

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
