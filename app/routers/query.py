from fastapi import Query


class LessonQueryParams:
    def __init__(
        self,
        group_name: str | None = Query(
            None, description="Название группы, расписание которой вы хотите узнать"),
        teacher_name: str | None = Query(
            None, description="Имя преподавателя, расписание которого вы хотите узнать"),
        room_name: str | None = Query(
            None, description="Название аудитории, расписание которой вы хотите узнать"),
        discipline_name: str | None = Query(
            None, description="Название группы, расписание которой вы хотите узнать"),

        specific_week: int | None = Query(
            None, description="Определенная неделя, например 1, 3 или 6"),
        week: int | None = Query(
            None, description="Расписание нечетной недели - 1, расписание нечетной - 2"),
        day_of_week: int | None = Query(
            None, description="Номера дней недели идут по порядку: 1 - понедельник, 2 - вторник и т.д."),

        period_id: int | None = Query(
            None, description="id периода, не изменяется, id интересующего периода можно посмотреть в '/period/'"),
        lesson_type_id: int | None = Query(
            None, description="id типов урока, не изменяется, id интересующего типа урока можно посмотреть в '/lesson_type/'"),
        call_id: int | None = Query(
            None, description="id звонков (номеров пар), не изменяется, id интересующего звонка можно посмотреть в '/call/'"),

        is_usual_place: bool = Query(
            None, description="Пара проводиться в кампусе, который является основным местом проведения занятий для этой группы"),

        skip: int = Query(
            None, description="Сколько объектов необходимо пропустить для ответа. Параметр для выгрузки расписания по частям."),
        limit: int = Query(
            None, description="Максимальное количество объектов в ответе. Не больше 1000. Не рекомендуется использовать значения больше 200 при работе c openapi. Параметр для выгрузки расписания по частям."),
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
        self.is_usual_place = is_usual_place
        self.skip = skip
        self.limit = limit
