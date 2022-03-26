from sqlalchemy.orm import Session
from .get_or_create import get_or_create
from ...database import models


def create_predefined(db: Session):

    def append_from_array(array, session, model):
        for el in array:
            id, short_name, name = el
            get_or_create(session=session, model=model, id=id,
                          short_name=short_name, name=name)

    def append_from_dict(diction, session, model):
        for key, value in diction.items():
            get_or_create(session=session, model=model, id=value, name=key)
            # session.add(instance)
            # session.commit()

    inst = [
        {"id": 1, "name": "Институт перспективных технологий и индустриального программирования",
            "short_name": "ИПТИП"},
        {"id": 2, "name": "Институт технологий управления", "short_name": "ИТУ"},
        {"id": 3, "name": "Институт информационных технологий", "short_name": "ИИТ"},
        {"id": 4, "name": "Институт искусственного интеллекта", "short_name": "ИИИ"},
        {"id": 5, "name": "Институт кибербезопасности и цифровых технологий",
         "short_name": "ИКБ"},
        {"id": 6, "name": "Институт радиоэлектроники и информатики",
         "short_name": "ИРЭИ"},
        {"id": 7, "name": "Институт тонких химических технологий им. М.В. Ломоносова",
         "short_name": "ИТХТ"},
    ]
    places = [[1, 'В-78', 'Проспект Вернадского, д.78'],
              [2, 'В-86', 'Проспект Вернадского, д.86'],
              [3, 'С-20', 'Стромынка, д.20'],
              [4, 'МП-1', 'Малая Пироговская, д.1'],
              [5, 'СГ-22', '5-я ул. Соколиной горы, д.22']
              ]
    calls = [[1, {"begin_time": '9:00', "end_time": '10:30'}, 1],
             [2, {"begin_time": '10:40', "end_time": '12:10'}, 2],
             [3, {"begin_time": '12:40', "end_time": '14:10'}, 3],
             [4, {"begin_time": '14:20', "end_time": '15:50'}, 4],
             [5, {"begin_time": '16:20', "end_time": '17:50'}, 5],
             [6, {"begin_time": '18:00', "end_time": '19:30'}, 6],
             [7, {"begin_time": '19:40', "end_time": '21:10'}, 7],
             [8, {"begin_time": '18:30', "end_time": '20:00'}, 7],
             [9, {"begin_time": '20:10', "end_time": '21:40'}, 8],
             ]

    lesson_types_for_creation = [
        [1, "лк", "Лекция"],
        [2, "пр", "Практическое занятие"],
        [3, "лр", "Лабораторная работа"],
        [4, "зач", "Зачёт"],
        [5, "экз", "Экзамен"],
        [6, "кр", "Курсовая работа"],
        [7, "зд", "Дифференцированный зачет"],
        [8, "срс", "Самостоятельная работа студента"],
    ]
    periods_for_creation = [
        [1, "semester", "Учебный семестр"],
        [2, "credits", "Зачетная сессия"],
        [3, "exams", "Экзаменационная сессия"],
    ]

    degrees = {
        "Бакалавриат": 1,
        "Магистратура": 2,
        "Специалитет": 3
    }

    append_from_array(places, db, models.Place)
    append_from_array(lesson_types_for_creation, db, models.LessonType)
    append_from_array(periods_for_creation, db, models.Period)

    for el in calls:
        id, time, call_num = el
        get_or_create(session=db, model=models.Call, id=id, call_num=call_num,
                      begin_time=time["begin_time"], end_time=time["end_time"])
    for el in inst:
        get_or_create(session=db, model=models.Institute,
                      id=el['id'], name=el['name'], short_name=el['short_name'])

    append_from_dict(degrees, db, models.Degree)
    db.commit()
    pass
