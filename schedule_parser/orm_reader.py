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
from .get_or_create import get_or_create
from . import models


class Reader:

    def __init__(self, without_weeks):
        self.without_weeks = without_weeks

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
            "semestr": 1,
            "credits": 2,
            "exams": 3
        }

        self.current_place = 1
        self.current_period = 1

    def run(self, xlsx_dir):

        for path, dirs, files in os.walk(xlsx_dir):

            for file_name in files:

                file_name = file_name.lower()
                if "стром" in file_name or "кбисп" in file_name:
                    self.current_place = 3
                elif "итхт" in file_name:
                    self.current_place = 2
                else:
                    self.current_place = 1
                
                self.current_period = self.periods[path.split("\\")[1]]
                print("current_period -> ", self.current_period)
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

    def format_teacher_name(self, cell):
        # TODO add re.sub here
        cell = str(cell)
        res = re.split(r'\n|\\\\|\\|(?!\d)\/(?!\d)|(?<!\d)\/(?=\d)', cell)
        if len(res) > 1:
            res = [x.strip() for x in res if len(x.strip())]
        # print(res)
        return res

    def format_lesson_type(self, cell):
        result = re.split(';|\n|\\\\|\\|\s{1,}', cell)
        result = [x.strip() for x in result if len(x.strip())]
        # print(result, "result")
        return result

    def format_room_name(self, cell, correct_max_len):
        def check_room_for_78(room_name):
            return (re.match(r'^\w{1}-\d{1,3}$', room_name)
                    or re.match(r'^\w{1}-\d{1,3}\w{1}$', room_name)
                    or re.match(r'^\w{1}-\d{3}-\w{1}$', room_name)
                    or re.match(r'^\w{1}-\d{3}.\w{1}$', room_name)
                    or re.match(r'^\w{1}-\d{3}\(\w{1}\)$', room_name)
                    or re.match(r'^ИВЦ-\d{3}$', room_name)
                    or re.match(r'^\w{1}-\d{1}$', room_name)
                    or re.match(r'^ИВЦ-\d{3}-\w{1}$', room_name)
                    or re.match(r'^ИВЦ-\d{3}.\w{1}$', room_name))

        def format_78(room_name):
            def check_re(room_name):
                return (not re.match(r'^\w{1}-\d{1,3}$', room_name)
                        and not re.match(r'^\w{1}-\d{3}-\w{1}$', room_name)
                        and not re.match(r'^ИВЦ-\d{3}$', room_name)
                        and not re.match(r'^\w{1}-\d{1}$', room_name)
                        and not re.match(r'^ИВЦ-\d{3}-\w{1}$', room_name))
            if re.match(r'^\D\d', room_name) and not re.match(r"^\w-\d", room_name):
                room_name = re.sub(r'^(\w)', r'\g<1>-', room_name)
            # if re.match(r'^А', room_name) and not "А-" in room_name:
            #     room_name = re.sub(r'А', 'А-', room_name)
            # if re.match(r'^Г', room_name) and not "Г-" in room_name:
            #     room_name = re.sub(r'Г', 'Г-', room_name)

            if re.match(r'^\w{1}-\d{3}\w{1}$', room_name):
                print('convert', room_name, 'to', re.sub(
                    r'(^\w{1}-\d{3})(\w{1})$', r'\g<1>-\g<2>', room_name))
                room_name = re.sub(
                    r'(^\w{1}-\d{3})(\w{1})$', r'\g<1>-\g<2>', room_name)

            if re.match(r'^\w{1}-\d{3}\.\w{1}$', room_name):
                print('convert', room_name, 'to',
                      re.sub(r'\.', '-', room_name))
                room_name = re.sub(r'\.', '-', room_name)

            if re.match(r'^\w{1}-\d{3}\(\w{1}\)$', room_name):
                print('convert', room_name, 'to', re.sub(
                    r'\((\w{1})\)', '-\g<1>', room_name))
                room_name = re.sub(r'\((\w{1})\)', '-\g<1>', room_name)

            if re.match(r'^ИВЦ-\d{3}\.\w{1}$', room_name):
                print('convert', room_name, 'to',
                      re.sub(r'\.', '-', room_name))
                room_name = re.sub(r'\.', '-', room_name)

            if check_re(room_name):
                print('not match', room_name)

            return room_name

        if isinstance(cell, float):
            cell = int(cell)
        string = str(cell)

        string = string.replace('*', '').upper()

        for pattern in self.notes_dict:
            regex_result = re.findall(pattern, string, flags=re.A)
            for reg in regex_result:
                pattern = re.compile(r"%s *\n" % reg)
                # print(pattern.findall(string), "<- Found in ", string,)
                string = pattern.sub(reg, string)
        if self.current_place == 2: 
            rooms = re.split(r'(?<!КБ-1)(?<!КБ)(?<!КАФ)(?<!КАФ.)\n|\\\\|\\|\/|\t|\s{3,}|,', string)
            if len(rooms)<correct_max_len:
                rooms = re.split(r'(?<!КБ-1)(?<!КБ)(?<!КАФ)(?<!КАФ.)\s|\\\\|\\|\/|,', string)
        else:
            rooms = re.split(r'(?<!КБ-1)(?<!КБ)(?<!КАФ)\n|\\\\|\\|\/|\t|\s{3,}|,', string)
            if len(rooms)<correct_max_len:
                rooms = re.split(r'(?<!КБ-1)(?<!КБ)(?<!КАФ)\s|\\\\|\\|\/|,', string)

        # print(rooms)
        all_rooms = []

        if len(rooms) > 1:
            res = [x.strip() for x in rooms if len(x.strip())]
            

        # print(rooms)
        # print(len(rooms), rooms)
        for room_num in range(len(rooms)):
            
            res = None
            room = rooms[room_num].strip()
            if "КАФ." in room:
                room = re.sub(
                    r'КАФ.', r'КАФ', room)
            if "НА" in room:
                room = re.sub(
                    r'НА', r'', room).strip()

            if "КАФЕДРА" in room:
                room = re.sub(
                    r'КАФЕДРА', r'КАФ', room)

            for pattern in self.notes_dict.keys():
                regex_result = re.findall(pattern, room)
                if regex_result:
                    res = regex_result[0]

            if res:
                room = re.sub(res, "", room)
                # print("room", room.strip())
                if (self.notes_dict[res] == 1):
                    if re.match(r'^\d{2,}', room):
                        all_rooms.append([room.strip(), self.notes_dict[res]])
                    room = format_78(room)
                    
                all_rooms.append([room.strip(), self.notes_dict[res]])
            else:
                if room == "Д" or room == "Д." or "ДИСТ" in room or "ЛК Д" in room or not len(room):
                    all_rooms.append([room, None])
                elif self.current_place == 3 and check_room_for_78(room) or self.current_place == 3 and room[0] == "Е":
                    print("78 in strom!", room)
                    all_rooms.append([format_78(room), 1])
                elif self.current_place == 1:
                    all_rooms.append([format_78(room), 1])
                else:
                    all_rooms.append([room, self.current_place])
        # print(all_rooms, "<- all_rooms")
        return all_rooms

    def format_name(self, temp_name):
        """
        """
        temp_name = temp_name.strip()
        # print(temp_name, "temp_name")
        if not temp_name:
            return None
        # print(temp_name)
        result = re.split(';|\n|\\\\|\\|(?<!п)/(?!г)|(?<!п)/|/(?!г)', temp_name)
        
        result = [x.strip() for x in result if len(x.strip())]
        # print(result)
        for name_num in range(1, len(result)):

            if re.search(r'\d+\s+\d+|\d+,\s*\d+|\d+\s*,\d+', result[name_num]) and not re.search(r'\w{5,}', result[name_num]):
                clear_name = re.sub(r"\d+|п/г|\(|\)|,| н |н\.",
                                    "", result[name_num-1]).strip()

                # print(clear_name, "<- clear_name")
                result[name_num] += " " + clear_name

        for name_num in range(0, len(result)-1):
            if re.search(r'\d+\s+\d+|\d+,\s*\d+|\d+\s*,\d+', result[name_num]) and not re.search(r'\w{5,}', result[name_num]):
                clear_name = re.sub(r"\d+|п/г|\(|\)|,| н |н\.",
                                    "", result[name_num+1]).strip()
                if not re.search(r'\w{5,}', clear_name) and name_num+2 < len(result):
                    clear_name = re.sub(
                        r"\d+|п/г|\(|\)|,| н |н\.", "", result[name_num+2]).strip()
                # print(clear_name, "<- clear_name")
                result[name_num] += " " + clear_name

        # print(temp_name, "<- temp_name")
        # print(result)

        return result

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

        def data_append_to_lesson_without_weeks(group, period, teacher, day_num,
                                  call,
                                  week, lesson_type, room, discipline_name):


            discipline = get_or_create(
                session=db.session, model=models.Discipline, name=discipline_name)
            db.session.flush()
            lesson = models.Lesson(call_id=call, period_id=period,
                                   teacher_id=teacher, lesson_type_id=lesson_type,
                                   subgroup=None, discipline_id=discipline.id,
                                   room_id=room, group_id=group,
                                   day_of_week=day_num, week=week)
            db.session.add(lesson)
            db.session.flush()

        def data_append_to_lesson(group, period, teacher, day_num,
                                  call,
                                  week, lesson_type, room, discipline_name):

            weeks = []
            less = ""

            clean_discipline_name = re.sub(r"(?<!\+)\d+(?! *п/г)(?! *гр)(?! *\+)|,| н |н\.| кр |кр.|^кр |^н |-","", discipline_name).strip()
            if clean_discipline_name[0] == "н":
                clean_discipline_name = clean_discipline_name[1:]

            # if "кр." in discipline_name:
            #     exc = discipline_name.split("н.")[0]
            #     less = discipline_name.split("н.")[1].strip()
            #     regex_num = re.compile(r'\d+')
            #     weeks = [int(item) for item in regex_num.findall(exc)]

            #     # usless
            #     # if "-" in exc:
            #     #     weeks = range(2, 16, 2)
            #     #     .extend(L)
            #     #     weeks = range(2, 16, 2)
            #     # else:
            #     #     pass

            # elif " н." in discipline_name or " н " in discipline_name or ("н." in discipline_name and "Ин." not in discipline_name):
            #     if " н." in discipline_name:
            #         exc = discipline_name.split(" н.")[0]
            #         less = discipline_name.split(" н.")[1].strip()
            #     elif "н." in discipline_name:
            #         exc = discipline_name.split("н.")[0]
            #         less = discipline_name.split("н.")[1].strip()
            #     elif " н " in discipline_name:
            #         exc = discipline_name.split(" н ")[0]
            #         less = discipline_name.split(" н ")[1].strip()
            #     regex_num = re.compile(r'\d+')
            #     weeks = [int(item) for item in regex_num.findall(exc)]

                # if "-" in exc:

                #     weeks = list(range(weeks[0], weeks[1], 17))
                #     pass

            # else:
            #     less = discipline_name
            #     if int(week) % 2 == 1:
            #         weeks = list(range(1, 17, 2))

            #     else:
            #         weeks = list(range(2, 17, 2))

            discipline = get_or_create(
                session=db.session, model=models.Discipline, name=clean_discipline_name)
            db.session.flush()
            lesson = models.Lesson(call_id=call, period_id=period,
                                   teacher_id=teacher, lesson_type_id=lesson_type,
                                   subgroup=None, discipline_id=discipline.id,
                                   room_id=room, group_id=group,
                                   day_of_week=day_num)
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
                            if dist['name'].strip() == "":
                                continue

                            if "пр" in dist['type'].lower():
                                lesson_type = self.lesson_types["пр"]
                            if "лк" in dist['type'].lower():
                                lesson_type = self.lesson_types["лк"]
                            if "лаб" in dist['type'].lower():
                                lesson_type = self.lesson_types["лр"]
                            if "лр" in dist['type'].lower():
                                lesson_type = self.lesson_types["лр"]
                            if "лек" in dist['type'].lower():
                                lesson_type = self.lesson_types["лк"]

                            else:
                                lesson_type = self.lesson_types[""]

                            teacher = get_or_create(
                                session=db.session, model=models.Teacher, name=dist['teacher'][:49])
                            room = get_or_create(
                                session=db.session, model=models.Room, name=dist['room'][0], place_id=dist['room'][1])

                            db.session.flush()
                            occupation = 1
                            if(self.without_weeks):
                                data_append_to_lesson_without_weeks(group.id, occupation, teacher.id,
                                                    day_num,
                                                    call_num,
                                                    week, lesson_type, room.id, dist['name'])
                            else:
                                data_append_to_lesson(group.id, occupation, teacher.id,
                                                    day_num,
                                                    call_num,
                                                    week, lesson_type, room.id, dist['name'])

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

                tmp_name = self.format_name(tmp_name)

                if isinstance(tmp_name, list) and tmp_name:
                    

                    lesson_type = self.format_lesson_type(sheet.cell(
                        string_index, discipline_col_num + 1).value)

                    correct_max_len = max(len(tmp_name), len(lesson_type))


                    teacher = self.format_teacher_name(sheet.cell(
                        string_index, discipline_col_num + 2).value)
                    room = self.format_room_name(sheet.cell(
                        string_index, discipline_col_num + 3).value, correct_max_len)

                    # if ((len(room) > len(tmp_name) and len(room) > len(lesson_type)) and len(room) == 2 
                    #         and ("КБ" in room[0] or "каф" in room[0]) ):
                    #     room = [[room[0][0] + ' ' + room[1][0], room[0][1]]]
                        # print("!!!!!!!!!!!!!", room)
                    
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

        def get_day_num(day_name):
            """

            """
            return self.days_dict[day_name.upper()]


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
                    day_num_val = get_day_num(day_num_col.value)

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

        book = xlrd.open_workbook(xlsx_path, on_demand=True)
        sheet = book.sheet_by_index(0)
        DOC_TYPE_EXAM = 2
        column_range = []
        timetable = {}
        group_list = []

        # Индекс строки с названиями групп
        group_name_row_num = 1
        # TODO find by name of groups
        # v86 = ["", "", "", "", "", "", ""]
        # strom = ["УПБ", "УУБ", "УНБ", "УЮБ", "УМБ", "УЭБ", "", "", "", "", "", "", ""]
        for row_index in range(len(sheet.col(1))):
            group_name_row = sheet.row_values(row_index)
            if len(group_name_row) > 0:
                group_row_str = " ".join(str(x) for x in group_name_row)
                gr = re.findall(r'([А-Я]+-\w+-\w+)', group_row_str, re.I)
                if gr:
                    # group = gr[0][0:3]

                    # if group in v86:
                    #     self.current_place=2
                    # elif group in strom:
                    #     self.current_place=3
                    # else:
                    #     self.current_place=1
                    group_name_row_num = row_index
                    break

        group_name_row = sheet.row(group_name_row_num)

        for group_cell in group_name_row:  # Поиск названий групп
            group = str(group_cell.value)
            group = re.search(r'([А-Я]+-\w+-\w+)', group)
            if group:  # Если название найдено, то получение расписания этой группы
                print(group.group(0))
                if ("ТЛБО" in group.group(0) or "ЭСБО" in group.group(0)) and self.current_place == 2:
                    print("! ТЛБО or ЭСБО in group and current_place == 2")
                    continue
                # обновляем column_range, если левее группы нет разметки с неделями, используем старый
                if not group_list:
                    column_range = get_column_range_for_type_eq_semester(
                        sheet, group_cell, group_name_row_num)

                group_list.append(group.group(0))

                # if doc_type != DOC_TYPE_EXAM:
                one_time_table = self.read_one_group_for_semester(
                    sheet, group_name_row.index(group_cell), group_name_row_num, column_range)  # По номеру столбца

                # print(one_time_table)

                for key in one_time_table.keys():
                    # Добавление в общий словарь
                    timetable[key] = one_time_table[key]

        self.write_to_db(timetable)
        book.release_resources()
        del book
        return group_list
