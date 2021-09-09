import re
import json
import os.path
import subprocess
import datetime
import traceback
import xlrd

from itertools import cycle
from app import db
from . import get_or_create
from . import models

class Reader:
    """Класс для парсинга расписания MIREA из xlsx файлов"""


    def __init__(self):
        """Инициализация клсса
            src(str): Абсолютный путь к XLS файлу
        """

        self.notes_dict = {
            'МП-1': "ул. Малая Пироговская, д.1",
            'В-78': "Проспект Вернадского, д.78",
            'В-86': "Проспект Вернадского, д.86",
            'С-20': "ул. Стромынка, 20",
            'СГ-22': "5-я ул. Соколиной горы, д.22"
        }

        self.doc_type_list = {
            'semester': 0
        }

        self.days_dict = {
            'ПОНЕДЕЛЬНИК': 1,
            'ВТОРНИК': 2,
            'СРЕДА': 3,
            'ЧЕТВЕРГ': 4,
            'ПЯТНИЦА': 5,
            'СУББОТА': 6
        }

        self.months_dict = {
            'ЯНВАРЬ': 1,
            'ФЕВРАЛЬ': 2,
            'МАРТ': 3,
            'АПРЕЛЬ': 4,
            'МАЙ': 5,
            'ИЮНЬ': 6,
            'ИЮЛЬ': 7,
            'АВГУСТ': 8,
            'СЕНТЯБРЬ': 9,
            'ОКТЯБРЬ': 10,
            'НОЯБРЬ': 11,
            'ДЕКАБРЬ': 12
        }

        self.time_dict = {
            "9:00": 1,
            "10:40": 2,
            "12:40": 3,
            "14:20": 4,
            "16:20": 5,
            "18:00": 6,
            "18:30": 7,
            "20:10": 8
        }
        
        self.lesson_types = {
            "лк": 1,
            "пр": 2,
            "лаб": 3,
            "": 4,
        }
        
        self.periods = {
            "semestr": 1,
            "credits": 2,
            "exams": 3
        }

    def run(self, xlsx_dir,):

        def get_doc_type_code(doc_type_str):
            """
            Получение типа документа, для каждого типа документа
            :param doc_type_str:
            :return:
            """
            return self.doc_type_list[doc_type_str]

        ######TODO connect
        # self.connect_to_old_db = sqlite3.connect(self.db_old_file)
        # self.connect_to_db = sqlite3.connect(self.db_file)

        for path, dirs, files in os.walk(xlsx_dir):
            
            for file_name in files:
                if "зима" in file_name or "лето" in file_name:
                    continue
                path_to_xlsx_file = os.path.join(path, file_name)
                print(path_to_xlsx_file)
                # if("ИКиб_маг_2к" in path_to_xlsx_file):
                #     continue
                xlsx_doc_type = get_doc_type_code(os.path.dirname(os.path.relpath(path_to_xlsx_file, start='xls')))

                try:
                    
                    self.read(path_to_xlsx_file, xlsx_doc_type)
                except Exception as err:
                    print(err, traceback.format_exc(), "in", file_name)
                    continue

    def read(self, xlsx_path, doc_type):
        """Объединяет расписания отдельных групп и записывает в файлы
            :param xlsx_path:
            :param doc_type:
            :return:
        """

        def get_day_num(day_name):
            """
            Получение номера дня недели
            :param day_name: Название дня недели в верхнем регистре
            :return:
            """
            return self.days_dict[day_name.upper()]

        def get_month_num(month_name):
            """
            Получение номера месяца
            :param month_name: Названеи месяца в верхнем регистре
            :return:
            """
            return self.months_dict[month_name.upper().replace(' ', '')]

        def get_column_range_for_type_eq_semester(xlsx_sheet, group_name_cell, group_name_row_index):
            """
            Получение диапазона ячеек недели для типа расписания = семестр
            :param group_name_row_index: 
            :param xlsx_sheet:
            :param group_name_cell:
            :return:
            """

            week_range = {
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: []
            }

            initial_row_num = group_name_row_index + 1  # Номер строки, с которой начинается отсчет пар
            lesson_count = 0  # Счетчик количества пар
            # Перебор столбца с номерами пар и вычисление на основании количества пар в день диапазона выбора ячеек
            day_num_val, lesson_num_val, lesson_time_val, lesson_week_num_val = 0, 0, 0, 0
            row_s = len(xlsx_sheet.col(group_name_row.index(group_name_cell)))
                
            for lesson_num in range(initial_row_num, row_s):

                day_num_col = xlsx_sheet.cell(lesson_num, group_name_row.index(group_name_cell) - 5)
                
                if day_num_col.value != '':
                    day_num_val = get_day_num(day_num_col.value)

                lesson_num_col = xlsx_sheet.cell(lesson_num, group_name_row.index(group_name_cell) - 4)
                if lesson_num_col.value != '':
                    lesson_num_val = lesson_num_col.value
                    if isinstance(lesson_num_val, float):
                        lesson_num_val = int(lesson_num_val)
                        if lesson_num_val > lesson_count:
                            lesson_count = lesson_num_val

                lesson_time_col = xlsx_sheet.cell(lesson_num, group_name_row.index(group_name_cell) - 3)
                if lesson_time_col.value != '':
                    lesson_time_val = str(lesson_time_col.value).replace('-', ':')

                lesson_week_num = xlsx_sheet.cell(lesson_num, group_name_row.index(group_name_cell) - 1)
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
                    lesson_range = (lesson_num_val, lesson_time_val, lesson_week_num_val, lesson_string_index)
                    week_range[day_num_val].append(lesson_range)
            return week_range

        
        book = xlrd.open_workbook(xlsx_path, on_demand = True)
        sheet = book.sheet_by_index(0)
        DOC_TYPE_EXAM = 2
        column_range = []
        timetable = {}
        group_list = []

        # Индекс строки с названиями групп
        group_name_row_num = 1
        # Поиск строки, содержащей названия групп
        leng = len(sheet.col(1))
        if leng > 200:
            leng = 122
        for row_index in range(leng):
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
                print(group.group(0))
                # обновляем column_range, если левее группы нет разметки с неделями, используем старый
                if not group_list and doc_type != DOC_TYPE_EXAM:
                    column_range = get_column_range_for_type_eq_semester(sheet, group_cell, group_name_row_num)


                group_list.append(group.group(0))

                if doc_type != DOC_TYPE_EXAM:
                    one_time_table = self.read_one_group_for_semester(
                        sheet, group_name_row.index(group_cell), group_name_row_num, column_range)  # По номеру столбца
               
                # print(one_time_table)

                for key in one_time_table.keys():
                    timetable[key] = one_time_table[key]  # Добавление в общий словарь

        write_to_db(doc_type, timetable)
        book.release_resources()
        del book
        return group_list

    @staticmethod
    def format_teacher_name(cell):
        cell = str(cell)
        return re.split(r' {2,}|\n', cell)

    def format_room_name(self, cell):
        if isinstance(cell, float):
            cell = int(cell)
        string = str(cell)
        for pattern in self.notes_dict:
            regex_result = re.findall(pattern, string, flags=re.A)
            if regex_result:
                string = string.replace('  ', '').replace('*', '').replace('\n', '')
                string = re.sub(regex_result[0], self.notes_dict[regex_result[0]] + " ", string, flags=re.A)

        return re.split(r' {2,}|\n', string)

    @staticmethod
    def format_name(temp_name):
        """Разбор строки 'Предмет' на название дисциплины и номера
            недель включения и исключения
            temp_name(str)
        """

        def if_diapason_week(lesson_string):
            start_week = re.findall(r"\d+\s+-", lesson_string)
            start_week = re.sub("-", "", start_week[0])
            end_week = re.findall(r"-\d+\s+", lesson_string)
            end_week = re.sub("-", "", end_week[0])
            weeks = []
            for week in range(int(start_week), int(end_week) + 1):
                weeks.append(week)
            return weeks

        result = []
        temp_name = temp_name.replace(" ", "  ")
        temp_name = temp_name.replace(";", ";  ")
        # print("1", temp_name)
        temp_name = re.sub(r"(\s+-\s+(?:лк|пр)(?:;|))", "", temp_name, flags=re.A)
        substr = re.findall(r"(\s+н(?:\.|)\s+)\d+", temp_name)
        if substr:
            temp_name = re.sub(substr[0], " ", temp_name, flags=re.A)

        temp_name = re.sub(r"(\d+)", r"\1 ", temp_name, flags=re.A)
        temp_name = re.sub(r"(кр\. {2,})", "кр.", temp_name, flags=re.A)

        temp_name = re.sub(r"((, *|)кроме {1,})", " кр.", temp_name, flags=re.A)
        temp_name = re.sub(r"(н[\d,. ]*[+;])", "", temp_name, flags=re.A)
        temp_name = re.findall(r"((?:\s*[\W\s]*)(?:|кр[ .]\s*|\d+\s+-\d+\s+|[\d,. ]*)\s*\s*(?:|[\W\s]*|\D*)*\s*(?:|\(\d\s+п/г\)))(?:\s\s|\Z|\n)",
                               temp_name, flags=re.A)
        # print("2", temp_name)
        if isinstance(temp_name, list):
            for item in temp_name:
                if len(item) > 0:
                    _except = ""
                    _include = ""
                    name = item
                    name = name.replace("  ", " ")
                    name = name.strip()
                    one_str = [name, _include, _except]
                    result.append(one_str)
        return result

    def get_lesson_num_from_time(self, time_str):
        if time_str in self.time_dict:
            return self.time_dict[time_str]
        else:
            return 0

    def write_to_db(self, doc_type, timetable):
        
        def append_from_dict(diction, session, model):
            for key, value in diction.items():
                instanse = model(value, key)
                session.add(instance)
                session.commit()

        def data_append_to_lesson(group_name, occupation, discipline_name, teacher_name, date, day_num,
                                  call_num,
                                  week, lesson_type, room_num, include, exception):
            
            call = 
            group = models.Grpup.query.filter_by(group_num=group_num).first()
            period = models.Period.query.get(occupation)
            discipline = models.Discipline.query.filter_by(name=discipline_name).first()
            teacher = models.Teacher.query.filter_by(teacher_name=teacher_name).first()
            lesson_type = models.LessonType.query.filter_by(lesson_type=lesson_type).first()
            room = models.Room.query.filter_by(group_num=group_num).first()
            
            lesson = models.Lesson()
            
            
        db_cursor = self.connect_to_db.cursor()

        append_from_dict(self.time_dict, db, models.Call)
        append_from_dict(self.lesson_types, db, models.LessonType)
        append_from_dict(self.periods, db, models.Period)
        
        for group_name, value in sorted(timetable.items()):

            group_name = re.findall(r"([А-Я]+-\w+-\w+)", group_name, re.I)
            if len(group_name) > 0:
                group_name = group_name[0]
                get_or_create(group_name, models.Group)

            for n_day, day_item in sorted(value.items()):
                for n_lesson, lesson_item in sorted(day_item.items()):
                    for n_week, item in sorted(lesson_item.items()):
                        day_num = n_day.split("_")[1]
                        call_num = n_lesson.split("_")[1]
                        week = n_week.split("_")[1]
                        for dist in item:
                            print(dist)
                            call_time = dist['time']
                            if "include" in dist:
                                include = str(dist["include"])[1:-1]
                            else:
                                include = ""
                            if "exception" in dist:
                                exception = str(dist["exception"])[1:-1]
                            else:
                                exception = ""

                            if write_to_db is not False:
                                get_or_create(dist['teacher'], modrls.Teacher) #### TODO
                                get_or_create(dist['name'], models.Discipline) ### TODO
                                get_or_create(dist['type'], models.LessonType) #### TODO
                                get_or_create(dist['room'], models.Room) #### TODO

                                occupation = 1
                                data_append_to_lesson(group_name, occupation, dist['name'], dist['teacher'],
                                                        day_num,
                                                        call_num,
                                                        week, dist['type'], dist['room'], include, exception) #### TODO

        self.connect_to_db.commit()
        db_cursor.close()


    def read_one_group_for_semester(self, sheet, discipline_col_num, group_name_row_num, cell_range):
        """
            Получение расписания одной группы
            discipline_col_num(int): Номер столбца колонки 'Предмет'
            range(dict): Диапазон выбора ячеек
        """
        one_group = {}
        group_name = sheet.cell(group_name_row_num, discipline_col_num).value  # Название группы
        one_group[group_name] = {}  # Инициализация словаря

        # перебор по дням недели (понедельник-суббота)
        # номер дня недели (1-6)
        for day_num in cell_range:
            one_day = {}

            for lesson_range in cell_range[day_num]:
                lesson_num = lesson_range[0]
                time = lesson_range[1]
                week_num = lesson_range[2]
                string_index = lesson_range[3]

                # Перебор одного дня (1-6 пара)
                if "lesson_{}".format(lesson_num) not in one_day:
                    one_day["lesson_{}".format(lesson_num)] = {}

                # Получение данных об одной паре
                tmp_name = str(sheet.cell(string_index, discipline_col_num).value)
                tmp_name = self.format_name(tmp_name)

                if isinstance(tmp_name, list) and tmp_name != []:

                    lesson_type = sheet.cell(string_index, discipline_col_num + 1).value
                    teacher = self.format_teacher_name(sheet.cell(string_index, discipline_col_num + 2).value)
                    room = self.format_room_name(sheet.cell(string_index, discipline_col_num + 3).value)

                    max_len = max(len(tmp_name), len(teacher), len(room))
                    if len(tmp_name) < max_len:
                        tmp_name = cycle(tmp_name)
                    if len(teacher) < max_len:
                        teacher = cycle(teacher)
                    if len(room) < max_len:
                        room = cycle(room)

                    lesson_tuple = list(zip(tmp_name, teacher, room))
                    for tuple_item in lesson_tuple:
                        name = tuple_item[0][0]
                        include = tuple_item[0][1]
                        exception = tuple_item[0][2]
                        teacher = tuple_item[1]
                        room = tuple_item[2]

                        if isinstance(room, float):
                            room = int(room)

                        one_lesson = {"date": None, "time": time, "name": name, "type": lesson_type,
                                      "teacher": teacher, "room": room}
                        if include:
                            one_lesson["include"] = include
                        if exception:
                            one_lesson["exception"] = exception

                        if name:
                            if "week_{}".format(week_num) not in one_day["lesson_{}".format(lesson_num)]:
                                one_day["lesson_{}".format(lesson_num)][
                                    "week_{}".format(week_num)] = []  # Инициализация списка
                            one_day["lesson_{}".format(lesson_num)]["week_{}".format(week_num)].append(one_lesson)

                    # Объединение расписания
                    one_group[group_name]["day_{}".format(day_num)] = one_day

        return one_group

if __name__ == "__main__":

    reader = Reader(path_to_db="table.db")
    reader.run('xls', write_to_db=True, write_to_new_db=True, write_to_json_file=False, write_to_csv_file=False)
