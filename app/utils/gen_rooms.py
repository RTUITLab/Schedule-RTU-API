import csv

from sqlalchemy.orm import Session
from ..database import models, schemas


def gen_rooms(db: Session):
    rooms = db.query(models.Room).all()
    header = ["номер комнаты", "корпус", "день недели",
              "номер пары", "неделя", "дисциплина", "группа"]
    days_of_week = {1: "понедельник", 2: "вторник",
                    3: "среда", 4: "четверг", 5: "пятница", 6: "суббота"}
    place_dict = {
        4: 'МП-1',
        1: 'В-78',
        2: 'В-86',
        3: 'С-20',
        5: 'СГ-22',
        None: 0
    }
    counter = 0
    with open('result.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, delimiter=";")
        writer.writeheader()
        for room in rooms:
            counter += 1
            if not counter % 100:
                print("...")
            if room.name == "КАФ" or room.name == "ФОК" or len(room.name.strip()) <= 1:
                continue
            lessons = room.lessons
            if not lessons:
                continue
            for lesson in room.lessons:
                disc = lesson.discipline.name
                sp = lesson.specific_weeks
                # if sp:
                #     disc = disc + " ("
                #     for i in sp:
                sp = [str(x.secific_week) for x in sp]
                sp = ", ".join(sp)
                groups = lesson.groups
                groups = [x.name for x in groups]
                for group in groups:

                    res = {"номер комнаты": room.name, "корпус": room.place.name,
                           "день недели": days_of_week[lesson.day_of_week], "номер пары": lesson.call_id, "неделя": lesson.week, "дисциплина": lesson.discipline.name + " (" + sp+")", "группа": group}
                writer.writerow(res)


def gen_rooms2(db: Session):
    rooms = db.query(models.Room).all()
    header = ["номер комнаты", "корпус", "день недели", "номер пары",
              "неделя", "определенные недели", "дисциплина", "группы"]
    days_of_week = {1: "понедельник", 2: "вторник",
                    3: "среда", 4: "четверг", 5: "пятница", 6: "суббота"}
    place_dict = {
        4: 'МП-1',
        1: 'В-78',
        2: 'В-86',
        3: 'С-20',
        5: 'СГ-22',
        None: 0
    }
    counter = 0
    with open('result.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, delimiter=";")
        writer.writeheader()
        for room in rooms:
            counter += 1
            if not counter % 100:
                print("...")
            if room.name == "КАФ" or room.name == "ФОК" or len(room.name.strip()) <= 1:
                continue
            lessons = room.lessons
            if not lessons:
                continue
            for lesson in room.lessons:
                disc = lesson.discipline.name
                sp = lesson.specific_weeks
                # if sp:
                #     disc = disc + " ("
                #     for i in sp:
                sp = [str(x.secific_week) for x in sp]
                groups = lesson.groups
                groups = [x.name for x in groups]

                res = {"номер комнаты": room.name, "корпус": room.place.name, "день недели": days_of_week[lesson.day_of_week], "номер пары": lesson.call_id, "неделя": lesson.week, "определенные недели": ", ".join(
                    sp), "дисциплина": lesson.discipline.name, "группы": ", ".join(groups)}
                writer.writerow(res)
