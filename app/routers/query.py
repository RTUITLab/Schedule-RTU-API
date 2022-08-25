from fastapi import Query
from typing import Optional


class LessonQueryParams:
    def __init__(
        self,
        group_name: Optional[str] = Query(
            None, description="Название группы, расписание которой вы хотите узнать"),
        teacher_name: Optional[str] = Query(
            None, description="Имя преподавателя, расписание которого вы хотите узнать"),
        room_name: Optional[str] = Query(
            None, description="Название аудитории, расписание которой вы хотите узнать"),
        discipline_name: Optional[str] = Query(
            None, description="Название группы, расписание которой вы хотите узнать"),

        specific_week: Optional[int] = Query(
            None, description="Определенная неделя, например 1, 3 или 6"),
        week: Optional[int] = Query(
            None, description="Расписание нечетной недели - 1, расписание нечетной - 2"),
        day_of_week: Optional[int] = Query(
            None, description="Номера дней недели идут по порядку: 1 - понедельник, 2 - вторник и т.д."),

        period_id: Optional[int] = Query(
            None, description="id периода, не изменяется, id интересующего периода можно посмотреть в '/periods"),
        lesson_type_id: Optional[int] = Query(
            None, description="id типа урока, не изменяется, id интересующего типа урока можно посмотреть в '/lesson_types'"),
        call_id: Optional[int] = Query(
            None, description="id звонка (номера пары), не изменяется, id интересующего звонка можно посмотреть в '/calls'"),
        place_id: Optional[int] = Query(
            None, description="id кампуса, не изменяется, id интересующего кампуса можно посмотреть в '/places'"),
        is_usual_place: bool = Query(
            None, description="Пара проводиться в кампусе, который является основным местом проведения занятий для этой группы"),

        skip: int = Query(
            None, description="Сколько объектов необходимо пропустить для ответа. Параметр для выгрузки расписания по частям."),
        limit: int = Query(
            None, description="Максимальное количество объектов в ответе. Не больше 600. Не рекомендуется использовать значения больше 200 при работе c openapi. Параметр для выгрузки расписания по частям."),
    ):
        self.group_name = group_name
        self.teacher_name = teacher_name
        self.room_name = room_name
        self.discipline_name = discipline_name
        self.specific_week = specific_week
        self.week = week
        self.day_of_week = day_of_week
        self.period_id = period_id
        self.lesson_type_id = lesson_type_id
        self.call_id = call_id
        self.place_id = place_id
        self.is_usual_place = is_usual_place
        self.skip = skip
        self.limit = limit


class DisciplineQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(
            None, description="Название дисциплины. Название можно вводить не полностью - в любом случае будет возвращен список совпадений")):
        self.name = name


class TeacherQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(
            None, description="Фамилия и инициалы преподавателя. Можно вводить только фамилию или только инициалы - в любом случае будет возвращен список совпадений")):
        self.name = name


class GroupQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(
            None, description="Название группы"),
        year: Optional[int] = Query(
            None, description="Курс группы (1-4)"),
        degree_id: Optional[int] = Query(
            None, description="id академической степени группы, не изменяется, id интересующей степени можно посмотреть в '/degrees'")):
        self.name = name
        self.year = year
        self.degree_id = degree_id


class RoomsQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(
            None, description="Название аудитории"),
        place_id: Optional[int] = Query(
            None, description="id кампуса, не изменяется, id интересующего кампуса можно посмотреть в '/places'")):
        self.name = name
        self.place_id = place_id
