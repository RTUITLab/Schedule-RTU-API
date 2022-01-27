import re


def format_teacher_name(cell):
    # TODO add re.sub here
    cell = str(cell)
    res = re.split(r'\n|\\\\|\\|(?!\d)\/(?!\d)|(?<!\d)\/(?=\d)', cell)
    if len(res) > 1:
        res = [x.strip() for x in res if len(x.strip())]
    # print(res)
    return res


def format_lesson_type(cell):
    result = re.split(';|\n|\\\\|\\|\s{1,}', cell)
    result = [x.strip() for x in result if len(x.strip())]

    # print(result, "result")
    return result


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

    for pattern in notes_dict:
        regex_result = re.findall(pattern, string, flags=re.A)
        for reg in regex_result:
            pattern = re.compile(r"%s *\n" % reg)
            # print(pattern.findall(string), "<- Found in ", string,)
            string = pattern.sub(reg, string)
    if current_place == 2:
        rooms = re.split(
            r'(?<!КБ-1)(?<!КБ)(?<!КАФ)(?<!КАФ.)\n|\\\\|\\|\/|\t|\s{3,}|,', string)
        if len(rooms) < correct_max_len:
            rooms = re.split(
                r'(?<!КБ-1)(?<!КБ)(?<!КАФ)(?<!КАФ.)\s|\\\\|\\|\/|,', string)
    else:
        rooms = re.split(
            r'(?<!КБ-1)(?<!КБ)(?<!КАФ)\n|\\\\|\\|\/|\t|\s{3,}|,', string)
        if len(rooms) < correct_max_len:
            rooms = re.split(
                r'(?<!КБ-1)(?<!КБ)(?<!КАФ)\s|\\\\|\\|\/|,', string)

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
                room = format_78(room)

            all_rooms.append([room.strip(), notes_dict[res]])
        else:
            if room == "Д" or room == "Д." or "ДИСТ" in room or "ЛК Д" in room or not len(room):
                all_rooms.append([room, None])
            elif current_place == 3 and check_room_for_78(room) or current_place == 3 and room[0] == "Е":
                print("78 in strom!", room)
                all_rooms.append([format_78(room), 1])
            elif current_place == 1:
                all_rooms.append([format_78(room), 1])
            else:
                all_rooms.append([room, current_place])
    # print(all_rooms, "<- all_rooms")
    return all_rooms


def format_name(temp_name, week, week_count):
    """
    """
    temp_name = re.sub(r'(\. \. )+|(\.\.\.)+|…+', '', temp_name)
    temp_name = temp_name.strip()
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
        if clean_discipline_name[0] == "н":
            clean_discipline_name=clean_discipline_name[1:]
        
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
                        
                        print("start", start, "  end", end)
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
            for i in range(week, week_count+1, 2):
                result_weeks.add(i)
            print(week)
        result[name_num] = [clean_discipline_name, result_weeks]
        print(discipl, "| result[name_num] -> ", result[name_num])


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
    # print(temp_name, "<- temp_name")
    # print(result)

    return result
