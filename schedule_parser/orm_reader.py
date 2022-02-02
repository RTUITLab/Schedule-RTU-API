from distutils.command.clean import clean
import re
import json
import os.path
import subprocess
import datetime
import traceback
import xlrd

from itertools import cycle
from app import db
from app.schedule import cur_week
from .get_or_create import get_or_create
from . import models
from .formatters import format_lesson_type, format_name, format_room_name, format_teacher_name


class Reader:

    def __init__(self):
        self.week_count = 16

        try:
            self.week_count = int(models.WorkingData.query.filter_by(name="week_count").first().value)

        except Exception as err:
            self.week_count = int(get_or_create(session=db.session, model=models.WorkingData,
                    name="week_count", value="16")).value

            print("week_count ERROR! -> ", err)

        
        self.notes_dict = {
            'МП-1': 4,
            'В-78': 1,
            'В-86': 2,
            'В78': 1,
            'С-20': 3,
            'СГ': 5,
            'СГ-22': 5,

        }
        self.notes_dict_for_creation = {
            'МП-1': 4,
            'В-78': 1,
            'В-86': 2,
            'С-20': 3,
            'СГ-22': 5
        }

        self.days_dict = {
            'ПОНЕДЕЛЬНИК': 1,
            'ВТОРНИК': 2,
            'СРЕДА': 3,
            'ЧЕТВЕРГ': 4,
            'ПЯТНИЦА': 5,
            'СУББОТА': 6
        }

        self.time_dict = {
            "9:00": 1,
            "10:40": 2,
            "12:40": 3,
            "14:20": 4,
            "16:20": 5,
            "18:00": 6,
            "19:40": 7,
            "18:30": 8,
            "20:10": 9
        }

        self.lesson_types_for_creation = {
            "лк": 1,
            "пр": 2,
            "лр": 3,
            "": 4,
            "зач": 5,
            "экз": 6,
            "кр": 7,
            "зд": 8,
        }

        self.lesson_types = {
            "лк": 1,
            "лек": 1,
            "пр": 2,
            "лр": 3,
            "лаб": 3,
            "": 4,
        }

        self.periods = {
            "semester": 1,
            "credits": 2,
            "exams": 3
        }

        self.current_place = 1
        self.current_period = 1
        # print("Reader initialized")

    def run(self, xlsx_dir):
        
        for path, dirs, files in os.walk(xlsx_dir):
            for file_name in files:

                file_name = file_name.lower()
                if "стром" in file_name or "кбисп" in file_name or "икб" in file_name:
                    self.current_place = 3
                elif "итхт" in file_name:
                    self.current_place = 2
                else:
                    self.current_place = 1
                try:
                    if ("\\") in path:
                        self.current_period = self.periods[path.split("\\")[1]]
                    else:
                        self.current_period = self.periods[path.split("/")[1]]
                except Exception as e:
                    print(e)
                    continue
                # print("current_period -> ", self.current_period)
                path_to_xlsx_file = os.path.join(path, file_name)
                print(path_to_xlsx_file)
                # if("ИКиб_маг_2к" in path_to_xlsx_file):
                #     continue

                try:
                    self.read(path_to_xlsx_file)
                    # TODO move truncate here
                    db.session.commit()
                except Exception as err:
                    print(err, traceback.format_exc(), "in", file_name)
                    continue

    def get_lesson_num_from_time(self, time_str):
        if time_str in self.time_dict:
            return self.time_dict[time_str]
        else:
            return 0

    def write_to_db(self, timetable):

        def append_from_dict(diction, session, model):
            for key, value in diction.items():
                get_or_create(session=session, model=model, id=value, name=key)
                # session.add(instance)
                # session.commit()

        def add_weeks(weeks, lesson):
            for week in weeks:
                week_l = models.LessonOnWeek(week=week, lesson=lesson)
                db.session.add(week_l)

        def data_append_to_lesson(group, period, teacher, day_num,
                                  call,
                                  week, lesson_type, room, is_usual_location, discipline_name):
            
                # print(discipline_name)
                weeks = list(discipline_name[1])
                weeks.sort()

                less = ""

                # print(discipline_name[0])

                discipline = get_or_create(
                    session=db.session, model=models.Discipline, name=discipline_name[0])
                db.session.flush()
                
                lesson = models.Lesson(call_id=call, period_id=period,
                                    teacher_id=teacher, lesson_type_id=lesson_type,
                                    subgroup=None, discipline_id=discipline.id,
                                    room_id=room, group_id=group,
                                    day_of_week=day_num, is_usual_location=is_usual_location)
                db.session.add(lesson)
                db.session.flush()
                add_weeks(weeks, lesson.id)


        append_from_dict(self.periods, db.session, models.Period)
        append_from_dict(self.time_dict, db.session, models.Call)
        append_from_dict(self.lesson_types_for_creation,
                         db.session, models.LessonType)
        append_from_dict(self.notes_dict_for_creation,
                         db.session, models.Place)

        stack = ""

        for group_name, value in sorted(timetable.items()):

            group_name = re.findall(r"([А-Я]+-\w+-\w+)", group_name, re.I)
            if len(group_name) > 0:
                print("Add schedule for ", group_name)
                group_name = group_name[0]

                group = get_or_create(session=db.session,
                                      model=models.Group, name=group_name)

            for n_day, day_item in sorted(value.items()):

                for n_lesson, lesson_item in sorted(day_item.items()):
                    for n_week, item in sorted(lesson_item.items()):
                        day_num = n_day.split("_")[1]
                        call_num = n_lesson.split("_")[1]
                        week = n_week.split("_")[1]
                        for dist in item:

                            if "пр" in dist['type'].lower():
                                lesson_type = self.lesson_types["пр"]
                            elif "лк" in dist['type'].lower():
                                lesson_type = self.lesson_types["лк"]
                            elif "лаб" in dist['type'].lower():
                                lesson_type = self.lesson_types["лр"]
                            elif "лр" in dist['type'].lower():
                                lesson_type = self.lesson_types["лр"]
                            elif "лек" in dist['type'].lower():
                                lesson_type = self.lesson_types["лк"]

                            else:
                                lesson_type = self.lesson_types[""]
    
                            teacher = get_or_create(
                                session=db.session, model=models.Teacher, name=dist['teacher'][:49])
                            room = get_or_create(
                                session=db.session, model=models.Room, name=dist['room'][0], place_id=dist['room'][1])

                            db.session.flush()

                            is_usual_location=True

                            if room.place_id == self.current_place or not room.place_id:
                                is_usual_location=True
                            else:
                                is_usual_location=False

                            # print(is_usual_location, room, room.place_id, self.current_place)

                            data_append_to_lesson(group.id, self.current_period, teacher.id,
                                                    day_num,
                                                    call_num,
                                                    week, lesson_type, room.id, is_usual_location, dist['name'])

    def read_one_group_for_semester(self, sheet, discipline_col_num, group_name_row_num, cell_range):
        """
            Получение расписания одной группы
            discipline_col_num(int): Номер столбца колонки 'Предмет'
            range(dict): Диапазон выбора ячеек
        """
        one_group = {}
        group_name = sheet.cell(
            group_name_row_num, discipline_col_num).value  # Название группы
        one_group[group_name] = {}  # Инициализация словаря

        # перебор по дням недели (понедельник-суббота)
        # номер дня недели (1-6)
        for day_num in cell_range:
            one_day = {}

            for lesson_range in cell_range[day_num]:
                lesson_num = lesson_range[0]
                time = lesson_range[1]
                if "18:30" in time:
                    lesson_num = 8
                if "19:40" in time:
                    lesson_num = 9
                week_num = lesson_range[2]
                string_index = lesson_range[3]

                # Перебор одного дня (1-6 пара)
                if "lesson_{}".format(lesson_num) not in one_day:
                    one_day["lesson_{}".format(lesson_num)] = {}

                # Получение данных об одной паре
                tmp_name = str(sheet.cell(
                    string_index, discipline_col_num).value)

                tmp_name = format_name(tmp_name, week_num, self.week_count)

                if isinstance(tmp_name, list) and tmp_name:

                    lesson_type = format_lesson_type(sheet.cell(
                        string_index, discipline_col_num + 1).value)

                    correct_max_len = max(len(tmp_name), len(lesson_type))

                    teacher = format_teacher_name(sheet.cell(
                        string_index, discipline_col_num + 2).value)
                    room = format_room_name(sheet.cell(
                        string_index, discipline_col_num + 3).value, correct_max_len, self.notes_dict, self.current_place)

                    # TODO need to fix
                    max_len = max(len(tmp_name), len(teacher),
                                  len(room), len(lesson_type))
                    if len(tmp_name) < max_len:
                        tmp_name = cycle(tmp_name)
                    if len(teacher) < max_len:
                        teacher = cycle(teacher)
                    if len(room) < max_len:
                        room = cycle(room)
                    if len(lesson_type) < max_len:
                        lesson_type = cycle(lesson_type)

                    lesson_tuple = list(
                        zip(tmp_name, teacher, room, lesson_type))

                    for tuple_item in lesson_tuple:
                        name = tuple_item[0]
                        teacher = tuple_item[1]
                        room = tuple_item[2]
                        lesson_type = tuple_item[3]

                        one_lesson = {"date": None, "time": time, "name": name, "type": lesson_type,
                                      "teacher": teacher, "room": room}

                        if name:
                            if "week_{}".format(week_num) not in one_day["lesson_{}".format(lesson_num)]:
                                one_day["lesson_{}".format(lesson_num)][
                                    "week_{}".format(week_num)] = []  # Инициализация списка
                            one_day["lesson_{}".format(lesson_num)]["week_{}".format(
                                week_num)].append(one_lesson)

                    # Объединение расписания
                    one_group[group_name]["day_{}".format(day_num)] = one_day
        # print(one_group)
        return one_group

    def read(self, xlsx_path):
        """

        """

        def get_column_range_for_type_eq_semester(xlsx_sheet, group_name_cell, group_name_row_index):
            week_range = {
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: []
            }

            # Номер строки, с которой начинается отсчет пар
            initial_row_num = group_name_row_index + 1
            lesson_count = 0  # Счетчик количества пар
            # Перебор столбца с номерами пар и вычисление на основании количества пар в день диапазона выбора ячеек
            day_num_val, lesson_num_val, lesson_time_val, lesson_week_num_val = 0, 0, 0, 0
            row_s = len(xlsx_sheet.col(group_name_row.index(group_name_cell)))

            for lesson_num in range(initial_row_num, row_s):

                day_num_col = xlsx_sheet.cell(
                    lesson_num, group_name_row.index(group_name_cell) - 5)

                if day_num_col.value != '':
                    day_num_val = self.days_dict[day_num_col.value.upper()]

                lesson_num_col = xlsx_sheet.cell(
                    lesson_num, group_name_row.index(group_name_cell) - 4)
                if lesson_num_col.value != '':
                    lesson_num_val = lesson_num_col.value
                    if isinstance(lesson_num_val, float):
                        lesson_num_val = int(lesson_num_val)
                        if lesson_num_val > lesson_count:
                            lesson_count = lesson_num_val

                lesson_time_col = xlsx_sheet.cell(
                    lesson_num, group_name_row.index(group_name_cell) - 3)
                if lesson_time_col.value != '':
                    lesson_time_val = str(
                        lesson_time_col.value).replace('-', ':')

                lesson_week_num = xlsx_sheet.cell(
                    lesson_num, group_name_row.index(group_name_cell) - 1)
                if lesson_week_num.value != '':
                    if lesson_week_num.value == 'I':
                        lesson_week_num_val = 1
                    elif lesson_week_num.value == 'II':
                        lesson_week_num_val = 2
                else:
                    if lesson_week_num_val == 1:
                        lesson_week_num_val = 2
                    else:
                        lesson_week_num_val = 1

                lesson_string_index = lesson_num

                if re.findall(r'\d+:\d+', str(lesson_time_val), flags=re.A):
                    lesson_range = (lesson_num_val, lesson_time_val,
                                    lesson_week_num_val, lesson_string_index)
                    week_range[day_num_val].append(lesson_range)
            return week_range

        book = xlrd.open_workbook(xlsx_path)
        sheet = book.sheet_by_index(0)
        DOC_TYPE_EXAM = 2
        column_range = []
        timetable = {}
        group_list = []

        # Индекс строки с названиями групп
        group_name_row_num = 1
        # TODO find by name of groups

        for row_index in range(len(sheet.col(1))):
            group_name_row = sheet.row_values(row_index)
            if len(group_name_row) > 0:
                group_row_str = " ".join(str(x) for x in group_name_row)
                gr = re.findall(r'([А-Я]+-\w+-\w+)', group_row_str, re.I)
                if gr:

                    group_name_row_num = row_index
                    break

        group_name_row = sheet.row(group_name_row_num)

        for group_cell in group_name_row:  # Поиск названий групп
            group = str(group_cell.value)
            group = re.search(r'([А-Я]+-\w+-\w+)', group)
            if group:  # Если название найдено, то получение расписания этой группы
                if ("ТЛБО" in group.group(0) or "ЭСБО" in group.group(0)) and self.current_place == 2:
                    print("! ТЛБО or ЭСБО in group and current_place == 2")
                    continue
                # обновляем column_range, если левее группы нет разметки с неделями, используем старый
                if not group_list:
                    
                    if self.current_period == 3:
                        continue
                    
                    elif self.current_period == 2 and self.current_place == 2: 
                        continue

                    elif self.current_period == 2:
                        continue
                    
                    else:
                        column_range = get_column_range_for_type_eq_semester(
                            sheet, group_cell, group_name_row_num)
                
                print(group.group(0))


                group_list.append(group.group(0))
                one_time_table = {}

                if self.current_period == 3:
                    pass

                elif self.current_period == 2 and self.current_place == 2: 
                    pass

                elif self.current_period == 2:
                    pass
                
                else:
                    one_time_table = self.read_one_group_for_semester(
                        sheet, group_name_row.index(group_cell), group_name_row_num, column_range)  # По номеру столбца

                for key in one_time_table.keys():
                    # Добавление в общий словарь
                    timetable[key] = one_time_table[key]

        self.write_to_db(timetable)
        book.release_resources()
        del book
        return group_list
