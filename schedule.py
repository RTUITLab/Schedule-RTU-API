# from connect import connect_to_sqlite
import datetime as dt
from datetime import datetime, date, time
from app import db
from schedule_parser import models

offset = dt.timedelta(hours=3)


rings = {
    1: {"start": '9:00', "end": '10:30'},
    2: {"start": '10:40', "end": '12:10'},
    3: {"start": '12:40', "end": '14:10'},
    4: {"start": '14:20', "end": '15:50'},
    5: {"start": '16:20', "end": '17:50'},
    6: {"start": '18:00', "end": '19:30'},
    7: {"start": '19:40', "end": '21:10'},
}

time_zone = dt.timezone(offset, name='МСК')

def cur_week(today):
    if today.month<8:
        first = date(today.year, 2, 9)
    else: 
        first = date(today.year, 9, 1)
    today_iso = today.isocalendar()
    first_iso = first.isocalendar()
    week = today_iso[1] - first_iso[1]
    
    if not (first_iso[2] == 7):
        week+=1
    return week

def return_one_day(today, gr):
    week = cur_week(today)
    result = []
    day_of_week = today.isocalendar()[2]
    
    
    day = [{
        "time" : {"start": '9:00', "end": '10:30'},
        "lesson": None
    }, {
        "time" : {"start": '10:40', "end": '12:10'},
        "lesson": None
    }, {
        "time" : {"start": '12:40', "end": '14:10'},
        "lesson": None
    }, {
        "time" :{"start": '14:20', "end": '15:50'} ,
        "lesson": None
    }, {
        "time" : {"start": '16:20', "end": '17:50'},
        "lesson": None
    }, {
        "time" : {"start": '18:00', "end": '19:30'},
        "lesson": None
    }, { 
        "time" : {"start": '19:40', "end": '21:10'},
        "lesson": None
    }]

    try:
        group = models.Group.query.filter_by(name=gr.strip()).first()
        print(str(group), gr)
        if not group:
            return None

        lessons = models.Lesson.query.filter_by(group_id=group.id, day_of_week=day_of_week)
        
        
        for lesson in lessons:
            a = models.LessonOnWeek.query.filter_by(week=week, lesson=lesson.id).first()
            if a:
                res_lesson = {}
                
                res_lesson["classRoom"] = models.Room.query.get(lesson.room_id).name
                res_lesson["teacher"] = models.Teacher.query.get(lesson.teacher_id).name
                res_lesson["name"] = models.Discipline.query.get(lesson.discipline_id).name
                res_lesson["type"] = models.LessonType.query.get(lesson.lesson_type_id).name
                
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
        res = {"bachelor": {"first":[], "second":[], "third":[], "fourth":[]},
                "master": {"first":[], "second":[]}
        }
        # cursor = connect_to_sqlite()
        record = models.Group.query.filter(models.Group.name.startswith('И')).all()
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
                if ind!=-1:
                    #res["master"][courses[course]][i]["numbers"].append({"number" : int(group[5:7]), "group": group})
                    res["master"][courses[course]][i]["numbers"].append(group)
                else:
                    #res["master"][courses[course]].append({"name": group[:4], "numbers":[{"number" : int(group[5:7]), "group": group}]})
                    res["master"][courses[course]].append({"name": group[:4], "numbers":[group]})

            elif group[2] == "Б":
                course = max_year - int(group[-2]+group[-1]) + 1
                ind = -1
                for i in range(len(res["bachelor"][courses[course]])):
                    if res["bachelor"][courses[course]][i]["name"] == group[:4]:
                        ind = i 
                if ind!=-1:
                    res["bachelor"][courses[course]][i]["numbers"].append(group)
                    #res["bachelor"][courses[course]][i]["numbers"].append({"number" : int(group[5:7]), "group": group})
                else:
                    res["bachelor"][courses[course]].append({"name": group[:4], "numbers":[group]})
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
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1) + dt.timedelta(days=7)
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
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1) + dt.timedelta(days=7)
        day = return_one_day(today, group)
        if day:
            res2[days[i]] = day
        else:
            return None     
    if cur_week(datetime.now(tz=time_zone))%2 == 1: 
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


def teacher_return_one_day(today, teacher_name):
    week = cur_week(today)
    day_of_week = today.isocalendar()[2]
    day = [{
        "time" : {"start": '9:00', "end": '10:30'},
        "lesson": None
    }, {
        "time" : {"start": '10:40', "end": '12:10'},
        "lesson": None
    }, {
        "time" : {"start": '12:40', "end": '14:10'},
        "lesson": None
    }, {
        "time" :{"start": '14:20', "end": '15:50'} ,
        "lesson": None
    }, {
        "time" : {"start": '16:20', "end": '17:50'},
        "lesson": None
    }, {
        "time" : {"start": '18:00', "end": '19:30'},
        "lesson": None
    }, { 
        "time" : {"start": '19:40', "end": '21:10'},
        "lesson": None
    }]

    try:
        teacher = models.Teacher.query.filter(models.Teacher.name==teacher_name).first()
        
        print(str(teacher), teacher_name)
        if not teacher:
            return None
        lessons = models.Lesson.query.filter_by(teacher_id=teacher.id, day_of_week=day_of_week)

        # lessons = models.Lesson.query.filter_by(group_id=group.id, day_of_week=day_of_week)
        for lesson in lessons:
            a = models.LessonOnWeek.query.filter_by(week=week, lesson=lesson.id).first()
            if a:
                res_lesson = {}
                
                res_lesson["classRoom"] = models.Room.query.get(lesson.room_id).name
                res_lesson["name"] = models.Discipline.query.get(lesson.discipline_id).name
                res_lesson["type"] = models.LessonType.query.get(lesson.lesson_type_id).name
                
                day[lesson.call_id-1]['lesson'] = res_lesson
                
    except Exception as e:
        print("Error", e)
        return None
    return day


def get_teachers():
    rows = models.Teacher.query.all()
    teachers = []
    for i in rows:
        teachers.append(i.name)
    return teachers


def teacher_today_sch(teacher):
    today = datetime.now(tz=time_zone)
    return teacher_return_one_day(today, teacher)


def teacher_tomorrow_sch(teacher): 
    today = datetime.now(tz=time_zone) + dt.timedelta(days=1)
    return teacher_return_one_day(today, teacher)


def teacher_week_sch(teacher): 
    today = datetime.now(tz=time_zone)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    for i in range(6):
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1)
        day = teacher_return_one_day(today, teacher)
        if day:
            res[days[i]] = day
        else:
            return None
    return res

def teacher_next_week_sch(teacher):
    today = datetime.now(tz=time_zone) + dt.timedelta(days=7)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    for i in range(6):
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1) + dt.timedelta(days=7)
        day = teacher_return_one_day(today, teacher)
        if day:
            res[days[i]] = day
        else:
            return None
    return res


def full_sched(teacher):
    today = datetime.now(tz=time_zone)
    day_of_week = today.isocalendar()[2]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    res = {}
    res2 = {}

    for i in range(6):
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1)
        day = teacher_return_one_day(today, teacher)
        if day:
            res[days[i]] = day
        else:
            return None
    for i in range(6):
        today = datetime.now(tz=time_zone) + dt.timedelta(days=i-day_of_week+1) + dt.timedelta(days=7)
        day = teacher_return_one_day(today, teacher)
        if day:
            res2[days[i]] = day
        else:
            return None     
    if cur_week(datetime.now(tz=time_zone))%2 == 1: 
        return {"first": res, "second": res2}
    return {"first": res2, "second": res}
# def get_day_teacher_schedule(teacher_name):
#     teacher = models.Teacher.query.filter(models.Teacher.name==teacher_name)
#     lessons = models.Lesson.query.filter_by(teacher_id=teacher.id)
    
#     teachers = []
#     for i in rows:
#         teachers.append(i.name)
#     return teachers


# def get_full_teacher_schedule(teacher_name):
#     teacher = models.Teacher.query.filter(models.Teacher.name==teacher_name)
#     lessons = models.Lesson.query.filter_by(teacher_id=teacher.id)
    
#     teachers = []
#     for i in rows:
#         teachers.append(i.name)
#     return teachers
