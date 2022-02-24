import re

from sqlalchemy import null


def format_teacher_name(cell):
    # TODO add re.sub here
    cell = str(cell).title()
    cell = re.sub(r'( ){3,}', '  ', cell)
    cell.strip()
    if not len(cell):
        return [None]
    res = re.split(r'\n|\\\\|\\|(?!\d)\/(?!\d)|(?<!\d)\/(?=\d)', cell)
    if len(res) > 1:
        res = [x.strip() for x in res if len(x.strip())]
    # print(res)
    return res


def format_lesson_type(cell):
    cell.strip()
    if not len(cell):
        return [None]

    result = re.split(';|\n|\\\\|\\|\s{1,}', cell)

    result = [x.strip() for x in result if len(x.strip())]

    # print(result, "result")
    return result


def room_fixer(room_name):
    if "КАФ." in room_name:
        room_name = re.sub(
            r'КАФ.', r'КАФ', room_name)
    if "НА" in room_name:
        room_name = re.sub(
            r'НА', r'', room_name).strip()

    if "КАФЕДРА" in room_name:
        room_name = re.sub(
            r'КАФЕДРА', r'КАФ', room_name)
    
    # and not re.match(r"[А-Я]-\d", room_name)

    if re.search(r'[А-Я]\d{1,3}', room_name):
        room_name = re.sub(r'([А-Я])(\d)', r'\g<1>-\g<2>', room_name)
    
    # if re.search(r'\d [А-Я],', room_name):
    #     room_name = re.sub(r'(\d) ([А-Я],)', r'\g<1>-\g<2>', room_name)
    
    if re.search(r'КБ-1', room_name) and not re.match(r"КБ-1 *№", room_name):
        room_name = re.sub(r'(КБ-1)', r'\g<1> №', room_name)

    if re.search(r'КБ-1', room_name) and not re.match(r"КБ-1 № +\d", room_name):
        room_name = re.sub(r'(КБ-1 №) +(\d)', r'\g<1>\g<2>', room_name)

    # if re.match(r'\d{3}', room_name):
    #     print(room_name) 

    # if re.match(r'\d{3}-[А-Я]{1}', room_name):
    #     print(room_name, re.sub(r'(\d{3})-([А-Я]{1})', r'\g<1>\g<2>', room_name))
    #     room_name = re.sub(r'(\d{3})-([А-Я]{1})', r'\g<1>\g<2>', room_name)
    if re.search(r'[А-Я]{1}-\d{1,3}[А-Я]{1}', room_name):
        room_name = re.sub(
            r'([А-Я]{1}-\d{1,3})([А-Я]{1})', r'\g<1>-\g<2>', room_name)

    if re.search(r'[А-Я]{1}-\d{3}\w{1}', room_name):
        # print('convert', room_name, 'to', re.sub(
        #     r'(^\w{1}-\d{3})(\w{1})$', r'\g<1>-\g<2>', room_name))
        room_name = re.sub(
            r'([А-Я]{1}-\d{3})(\w{1})', r'\g<1>-\g<2>', room_name)

    if re.search(r'[А-Я]{1}-\d{3}\.\w{1}', room_name):
        # print('convert', room_name, 'to',
        #       re.sub(r'\.', '-', room_name))
        room_name = re.sub(r'\.', '-', room_name)
    

    if re.search(r'[А-Я]{1}-\d{3}\(\w{1}\)', room_name):
        # print('convert', room_name, 'to', re.sub(
        #     r'\((\w{1})\)', '-\g<1>', room_name))
        room_name = re.sub(r'\((\w{1})\)', '-\g<1>', room_name)

    if re.search(r'ИВЦ-\d{3}\.\w{1}', room_name):
        # print('convert', room_name, 'to',
        #       re.sub(r'\.', '-', room_name))
        room_name = re.sub(r'\.', '-', room_name)

    return room_name


def format_room_name(cell, correct_max_len, notes_dict, current_place):
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

    if isinstance(cell, float):
        cell = int(cell)
    string = str(cell)

    string = re.sub(r'( ){3,}', '  ', string)

    string = string.replace('*', ' ').upper().strip()
    string = string.replace('\n', ' ')
    string = string.replace('ЛАБ', '')
    string = string.replace('ПР', '')
    if current_place == 2 and "ЕСЬ" in string:
        return [None]
    if not len(string):
        return [None]

    # # Убирает лишние символы между корпусом и аудиторией
    # for pattern in notes_dict:
    #     regex_result = re.findall(pattern, string, flags=re.A)
    #     for reg in regex_result:
    #         pattern = re.compile(r"%s *\n" % reg)
    #         string = pattern.sub(reg, string)
    
    if current_place == 2 and ":" in string:
        rooms = [string.split(":")[0]]
    else:
        string = room_fixer(string)
        rooms = re.findall(
            r'(МП-1)*(В78)*(С-20)*(СГ-22)*(СГ)*(В-86)*(В-78)* *(КАФ +[А-Я]+|КБ-1 *№\d*/\d*|КБ-1 *№\d*|ИВЦ-\d{3}-\w{1}|ИВЦ-\d{3}|[А-Я]{1}-\d{3}-\w{1}|\d{3}-[А-Я]{1}|[А-Я]{1}-\d{2,3}|\d{3}-[А-Я]{1}|\d{3}\.\d|\d{3}\w|\d{3}|[А-Я]{1}-\d-\w|[А-Я]{1}-\d|[А-Я]+|\d{2})',
            string)
        # print(string, rooms)
        rooms = [" ".join(y.strip() for y in x if y.strip()) for x in rooms]
        if not rooms:
            print("!!! Nothing was found in", string)

    # print(rooms)
    all_rooms = []

    if len(rooms) > 1:
        res = [x.strip() for x in rooms if len(x.strip())]

    # print(rooms)
    # print(len(rooms), rooms)
    for room_num in range(len(rooms)):

        res = None
        room = rooms[room_num].strip()

        for pattern in notes_dict.keys():
            regex_result = re.findall(pattern, room)
            if regex_result:
                res = regex_result[0]

        if res:
            room = re.sub(res, "", room)
            # print("room", room.strip())
            if (notes_dict[res] == 1):
                if re.match(r'^\d{2,}', room):
                    all_rooms.append([room.strip(), notes_dict[res]])
                room = room_fixer(room)

            all_rooms.append([room.strip(), notes_dict[res]])
        else:
            if room == "Д" or room == "Д." or "ДИСТ" in room or "ЛК Д" in room or not len(room):
                all_rooms.append([room, None])
            elif current_place == 3 and check_room_for_78(room) or current_place == 3 and room[0] == "Е":
                # print("78 in strom!", room)
                all_rooms.append([room_fixer(room), 1])
            elif current_place == 1:
                all_rooms.append([room_fixer(room), 1])
            else:
                all_rooms.append([room, current_place])
    # print(all_rooms, "<- all_rooms")
    return all_rooms


def format_name(temp_name, week, week_count):
    """
    """
    temp_name = re.sub(r'(\. \. )+|(\.\.\.)+|…+', '', temp_name)
    temp_name = re.sub(r'( ){3,}', '  ', temp_name)
    temp_name = temp_name.strip().capitalize()
    # print(temp_name, "temp_name")
    if len(temp_name) < 3:
        return ""
    # print(temp_name)
    temp_name = temp_name.replace('кроме', 'кр. ')

    result = re.split(';|\n|\\\\|\\|(?<!п)/(?!г)|(?<!п)/|/(?!г)', temp_name)

    result = [x.strip() for x in result if len(x.strip())]
    # print(result)
    for name_num in range(1, len(result)):

        if re.search(r'\d+\s+\d+|\d+,\s*\d+|\d+\s*,\d+', result[name_num]) and not re.search(r'\w{5,}', result[name_num]):
            clean_discipline_name = re.sub(r"п/гр|п/г|\(|\)|,|\d+н| н |н\.|(?<=\d)-(?= *\d)|(?<=\d )-(?= *\d)|\d+|\+|(?<!\w)нед\.*(?!\w)|(?<=\d)нед\.*(?!\w)",
                                           "", result[name_num-1]).strip()
            result[name_num] += " " + clean_discipline_name

    for name_num in range(0, len(result)-1):
        if re.search(r'\d+\s+\d+|\d+,\s*\d+|\d+\s*,\d+', result[name_num]) and not re.search(r'\w{5,}', result[name_num]):
            clean_discipline_name = re.sub(r"п/гр|п/г|\(|\)|,|\d+н| н |н\.|(?<=\d)-(?= *\d)|(?<=\d )-(?= *\d)|\d+|\+|(?<!\w)нед\.*(?!\w)|(?<=\d)нед\.*(?!\w)",
                                           "", result[name_num+1]).strip()
            if not re.search(r'\w{5,}', clean_discipline_name) and name_num+2 < len(result):
                clean_discipline_name = re.sub(
                    r"\d+|п/г|\(|\)|,| н |н\.", "", result[name_num+2]).strip()
            result[name_num] += " " + clean_discipline_name

    for name_num in range(len(result)):
        discipl = result[name_num]
        clean_discipline_name = re.sub(r"\d+н|(?<!\+)\d+(?! *п/г)(?! *гр)(?! *\+)|,| н |н\.| кр |кр\.|^кр |^н |(?<=\d)-(?= *\d)|(?<=\d )-(?= *\d)|(?<!\w)нед\.*(?!\w)|(?<=\d)нед\.*(?!\w)",
                                       "", discipl).strip()
        if len(clean_discipline_name) < 3:
            print("Something wrong with", temp_name, "! discipl ->",
                  discipl, "|clean_discipline_name->", clean_discipline_name)
            return ""
        if clean_discipline_name[0] == "н":
            clean_discipline_name = clean_discipline_name[1:]

        weeks = re.findall(
            r"(?<!\+)\d+(?! *п/г)(?! *гр)(?! *\+)|(?<=\d)-(?= *\d)|(?<=\d )-(?= *\d)", discipl)
        weeks = [i.strip() for i in weeks]
        # weeks = " ".join(weeks).strip()
        result_weeks = set()
        flag = 1

        if len(weeks):
            while "-" in weeks:
                indx = weeks.index("-")
                if indx and indx != len(weeks)-1:
                    try:
                        weeks.pop(indx)
                        end = int(weeks.pop(indx))
                        start = int(weeks.pop(indx - 1))

                        # print("start", start, "  end", end)
                        if start % 2 == 1 and week == 2 or start % 2 == 0 and week == 1:
                            start += 1

                        for i in range(start, end, 2):
                            result_weeks.add(i)

                        flag = 0
                    except Exception as e:
                        weeks.pop(indx)
                        print("BAD FORMAT -> ", discipl)
                else:
                    weeks.pop(indx)
                    print("BAD FORMAT -> ", discipl)
        if len(weeks):
            if re.search(r"(?<!\w)кр\.*(?!\w)|(?<!\w)кр\.*(?=\d)", discipl):
                for i in range(week, week_count+1, 2):
                    if str(i) not in weeks:
                        result_weeks.add(i)
            else:
                for i in weeks:
                    result_weeks.add(int(i))
        elif flag:
            # for i in range(week, week_count+1, 2):
            #     result_weeks.add(i)
            result_weeks = []
            # print(week)
        result[name_num] = [clean_discipline_name, result_weeks]
        # print(discipl, "| result[name_num] -> ", result[name_num])

    return result
