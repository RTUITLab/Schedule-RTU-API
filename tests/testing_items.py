from math import degrees


testing_items = {
    "calls":
    [
        {
            "call_num": 1,
            "begin_time": "9:00",
            "end_time": "10:30",
            "id": 1
        },
        {
            "call_num": 2,
            "begin_time": "10:40",
            "end_time": "12:10",
            "id": 2
        },
        {
            "call_num": 3,
            "begin_time": "12:40",
            "end_time": "14:10",
            "id": 3
        },
        {
            "call_num": 4,
            "begin_time": "14:20",
            "end_time": "15:50",
            "id": 4
        },
        {
            "call_num": 5,
            "begin_time": "16:20",
            "end_time": "17:50",
            "id": 5
        },
        {
            "call_num": 6,
            "begin_time": "18:00",
            "end_time": "19:30",
            "id": 6
        },
        {
            "call_num": 7,
            "begin_time": "19:40",
            "end_time": "21:10",
            "id": 7
        },
        {
            "call_num": 7,
            "begin_time": "18:30",
            "end_time": "20:00",
            "id": 8
        },
        {
            "call_num": 8,
            "begin_time": "20:10",
            "end_time": "21:40",
            "id": 9
        }
    ],
    "degrees":
    [
        {
            "name": "Бакалавриат",
            "id": 1
        },
        {
            "name": "Магистратура",
            "id": 2
        },
        {
            "name": "Специалитет",
            "id": 3
        }
    ],
    "disciplines":
    [
        {
            "name": "Правоведение",
            "id": 1
        },
        {
            "name": "Начертательная геометрия инженерная и компьютерная графика",
            "id": 2
        },
        {
            "name": "Линейная алгебра и аналитическая геометрия",
            "id": 3
        },
        {
            "name": "Физика",
            "id": 4
        },
        {
            "name": "Математическая логика и теория алгоритмов",
            "id": 5
        },
        {
            "name": "Ознакомительная практика",
            "id": 6
        },
        {
            "name": "Математический анализ",
            "id": 7
        },
        {
            "name": "Иностранный язык",
            "id": 8
        },
        {
            "name": "Физическая культура и спорт",
            "id": 9
        },
        {
            "name": "Объектно-ориентированное программирование",
            "id": 10
        },
        {
            "name": "Схемотехника устройств компьютерных систем",
            "id": 11
        },
        {
            "name": "Разработка предметно-ориентированных языков программирования",
            "id": 12
        },
        {
            "name": "Проектирование баз данных",
            "id": 13
        },
        {
            "name": "Анализ и концептуальное моделирование систем",
            "id": 14
        },
        {
            "name": "Программирование на языке Питон",
            "id": 15
        }
    ],
    "groups":
    [
        {
            "name": "ИВБО-01-21",
            "year": 1,
            "id": 1,
            "degree": {
                "name": "Бакалавриат",
                "id": 1
            }
        },
        {
            "name": "ИВБО-13-21",
            "year": 1,
            "id": 2,
            "degree": {
                "name": "Бакалавриат",
                "id": 1
            }
        }
    ],
    "lesson_types":
    [
        {
            "short_name": "лк",
            "name": "Лекция",
            "id": 1
        },
        {
            "short_name": "пр",
            "name": "Практическое занятие",
            "id": 2
        },
        {
            "short_name": "лр",
            "name": "Лабораторная работа",
            "id": 3
        },
        {
            "short_name": "зач",
            "name": "Зачёт",
            "id": 4
        },
        {
            "short_name": "экз",
            "name": "Экзамен",
            "id": 5
        },
        {
            "short_name": "кр",
            "name": "Курсовая работа",
            "id": 6
        },
        {
            "short_name": "зд",
            "name": "Дифференцированный зачет",
            "id": 7
        },
        {
            "short_name": "срс",
            "name": "Самостоятельная работа студента",
            "id": 8
        }
    ],
    "periods":
    [
        {
            "short_name": "semester",
            "name": "Учебный семестр",
            "id": 1
        },
        {
            "short_name": "credits",
            "name": "Зачетная сессия",
            "id": 2
        },
        {
            "short_name": "exams",
            "name": "Экзаменационная сессия",
            "id": 3
        }
    ],
    "places":
    [
        {
            "id": 1,
            "short_name": "В-78",
            "name": "Проспект Вернадского, д.78"
        },
        {
            "id": 2,
            "short_name": "В-86",
            "name": "Проспект Вернадского, д.86"
        },
        {
            "id": 3,
            "short_name": "С-20",
            "name": "Стромынка, д.20"
        },
        {
            "id": 4,
            "short_name": "МП-1",
            "name": "Малая Пироговская, д.1"
        },
        {
            "id": 5,
            "short_name": "СГ-22",
            "name": "5-я ул. Соколиной горы, д.22"
        }
    ],
    "rooms": [
        {
            "name": "А-401",
            "id": 1,
            "place": {
                "id": 4,
                "short_name": "МП-1",
                "name": "Малая Пироговская, д.1"
            }
        },
        {
            "name": "А-337",
            "id": 2,
            "place": {
                "id": 4,
                "short_name": "МП-1",
                "name": "Малая Пироговская, д.1"
            }
        },
        {
            "name": "Д",
            "id": 3,
            "place": None
        },
        {
            "name": "Г-112",
            "id": 4,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "А-403",
            "id": 5,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "А-150",
            "id": 6,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "В-331",
            "id": 7,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "И-305",
            "id": 8,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "КАФ",
            "id": 9,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "Г-109-Б",
            "id": 10,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "А-177-1",
            "id": 11,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "И-312",
            "id": 12,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "Г-111-Б",
            "id": 13,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "Г-109-А",
            "id": 14,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "И-202-А",
            "id": 15,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "А-302",
            "id": 16,
            "place": {
                "id": 4,
                "short_name": "МП-1",
                "name": "Малая Пироговская, д.1"
            }
        },
        {
            "name": "А-423",
            "id": 17,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        },
        {
            "name": "А-421",
            "id": 18,
            "place": {
                "id": 1,
                "short_name": "В-78",
                "name": "Проспект Вернадского, д.78"
            }
        }
    ],
    "teachers": [
        {
            "name": "Милкина Е.В.",
            "id": 1
        },
        {
            "name": "Верещагина Т.А.",
            "id": 2
        },
        {
            "name": "Ефремов А.В.",
            "id": 3
        },
        {
            "name": "Горшунова Т.А.",
            "id": 4
        },
        {
            "name": "Сафронов А.А.",
            "id": 5
        },
        {
            "name": "Воронцов А.А.",
            "id": 6
        },
        {
            "name": "Мусихин А.Г.",
            "id": 7
        },
        {
            "name": "Аксененкова И.М.",
            "id": 8
        },
        {
            "name": "Митин М.П.",
            "id": 9
        },
        {
            "name": "Козис Е.В.",
            "id": 10
        },
        {
            "name": "Попов А.М.",
            "id": 11
        },
        {
            "name": "Чугаева К.М.",
            "id": 12
        },
        {
            "name": "Беглов И.А.",
            "id": 13
        },
        {
            "name": "Ингтем Ж.Г.",
            "id": 14
        },
        {
            "name": "Слепухин Ю.А.",
            "id": 15
        },
        {
            "name": "Николаева С.В.",
            "id": 16
        },
        {
            "name": "Данилович Е.С.",
            "id": 17
        },
        {
            "name": "Урюпина Д.С.",
            "id": 18
        },
        {
            "name": "Прокопчук А.Р.",
            "id": 19
        },
        {
            "name": "Пономарев А.Н.",
            "id": 20
        },
        {
            "name": "Люлява Д.В.",
            "id": 21
        },
        {
            "name": "Семенов Р.Э.",
            "id": 22
        },
        {
            "name": "Смирнов Н.А.",
            "id": 23
        },
        {
            "name": "Богомольная Г.В.",
            "id": 24
        },
        {
            "name": "Воронков С.О.",
            "id": 25
        },
        {
            "name": "Ахмедова Х.Г.",
            "id": 26
        },
        {
            "name": "Советов П.Н.",
            "id": 27
        },
        {
            "name": "Макущенко М.А.",
            "id": 28
        },
        {
            "name": "Киселев Д.С.",
            "id": 29
        },
        {
            "name": "Володина А.М.",
            "id": 30
        }
    ]
}
