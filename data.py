import mysql.connector
import datetime
from tabulate import tabulate

TOKEN = '914271777:AAE0XrTZtXxQ8lnipXWKjPWtLb7Bn40kDMU'

conn = mysql.connector.connect(user='root', password='0000001', host='127.0.0.1', database='tgbot')
cursor = conn.cursor(buffered=True)

dict_of_data = {'login': '0', 'password': '0', 'grade': '0',
                'school_id': '0', 'grade_id': '0', 'name': '0',
                'stud_id': [], 'last_stud_id': '0', 'ad': '0',
                'subject': '0'}   # словарь с аудентификаторными данными
cancel_word = 'отмена'
back_word = 'Назад в админ. меню'
dict_of_admins = {704369002: "1",
                  }


def get_res(text):   # для получения рекламы
    cursor.execute('SELECT * FROM res')
    for i in cursor.fetchall():
        if text == i[0]:
            return i[1]


def get_list_of_schoold_for_admin():    # вывод школ для админа, назва + id
    cursor.execute('SELECT name_school, school_id FROM schools')
    result_str = ''
    for i in cursor.fetchall():
        result_str += i[0] + ' ID ' + i[1] + '\n'
    return result_str


def get_list_of_grades_for_admin():     # получение всех классов участвующих в проекте
    cursor.execute('SELECT schools.name_school, grades.number_grade, grades.school_id, '
                   'grades.grade_id FROM schools, grades '
                   'WHERE grades.school_id = schools.school_id')
    result_str = ''
    for i in cursor.fetchall():
        result_str += i[0] + ' Класс - ' + i[1] + ' Код - ' + i[2] + i[3] + '\n'
    return result_str


def get_list_of_schools():  # получение всех школ участвующих в проекте
    cursor.execute('SELECT name_school FROM schools')
    schools = cursor.fetchall()
    if not schools:
        return 'На данный момент школ участвующих в проекте нет.'
    result_str = ''
    for i in enumerate(schools):
        result_str += str(i[0] + 1) + ') ' + i[1][0] + '\n'
    return result_str


def get_grade(id):    # получение инфы о одном каком-либо классе
    if len(id) != 6:    # если не по форме сразу выкидыш
        return None
    school_id, grade_id = id[:3], id[3:]
    cursor.execute('SELECT * FROM schools, grades '
                   'WHERE schools.school_id = "{}" AND grades.grade_id = "{}"'.format(school_id, grade_id))
    # узнаем есть ли класс в проекте
    answer = cursor.fetchall()
    if len(answer) == 0:  # если класс введен неверно, выходим
        return None
    cursor.execute('SELECT * FROM grades WHERE grade_id = "{}"'.format(grade_id))  # получаем нужный класс
    ls_of_result = []   # создаем список, чтоб пихать туда весь собранный резуль, а именно:
    # расписание, учеников
    answer = cursor.fetchall()
    ls_of_result.append(answer[0])
    cursor.execute('SELECT * FROM timetable WHERE school_id = "{}" '
                   'AND grade_id = "{}"'.format(school_id, grade_id))
    try:
        answer = list(cursor.fetchall()[0][2:])
    except:
        return None
    try:
        answer[0] = 'Понедельник\n' + answer[0]
        answer[1] = 'Вторник\n' + answer[1]
        answer[2] = 'Среда\n' + answer[2]
        answer[3] = 'Четверг\n' + answer[3]
        answer[4] = 'Пятница\n' + answer[4]
        answer[5] = 'Суббота\n' + answer[5]
    except TypeError:
        answer = 'Полного расписания нет.'
    # настраиваем расписание
    ls_of_result.append(answer)
    dict_of_data['school_id'], dict_of_data['grade_id'] = id[:3], id[3:]
    return ls_of_result


def trans(today, timetable):
    # вывод самого расписания на определенный день по дню
    if today == 'Sunday':
        return 'Сегодня выходной :)'
    dict_of_days = {'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда',
                    'Thursday': 'Четверг', 'Friday': 'Пятница', 'Saturday': 'Суббота'}
    timetable = timetable[timetable.find(dict_of_days.get(today)):]
    timetable = timetable[:timetable.find('\n\n')]
    return timetable


def get_homework(timetable):    # добавление к расписанию на завтра ДЗшки
    result = timetable[:timetable.find('\n') + 1]
    timetable = timetable[timetable.find('\n') + 1:]
    while True:     # бежим по расписанию и сверяем его с бд, если есть ДЗ записываем его в новое раписание
        if timetable.find('\n') != -1:  # если есть перено, режем до переноски
            subject = timetable[:timetable.find('\n')]
        else:
            subject = timetable  # если предмет последний то не режем его
        cursor.execute('SELECT homework FROM homework WHERE school_id = "{}" AND grade_id = "{}" AND '
                       'subject = "{}"'.format(dict_of_data.get('school_id'), dict_of_data.get('grade_id'),
                                               subject))    # получаем дз
        try:
            homework = cursor.fetchall()[0][0]  # есть ли дз по предмету
        except IndexError:
            result += subject + ' : Задания нет.'
        else:
            result += subject + ' : ' + homework
        result += '\n'
        if timetable.find('\n') + 1 == 0:
            break   # если пробежались по всем предметам, выходим
        else:
            timetable = timetable[timetable.find('\n') + 1:]    # режем строку и следственно идем на некст предмет
    return result


def get_birthday():
    today = datetime.datetime.now().strftime("%d%m")
    cursor.execute('SELECT * FROM students WHERE school_id = "{}" AND grade_id = "{}"'.format(dict_of_data.get('school_id'),
                                                                                              dict_of_data.get('grade_id')))
    temp, result = 1, ''
    for i in cursor.fetchall():
        if i[3].find(today) == 0:
            result += str(temp) + '. ' + i[2] + ';\n'
            temp += 1
    if result:
        result = 'А сегодня,  день рождения отмечают:\n' + result
    return result


def get_timetable_on_tomorrow():
    # получение расписание на след. день, или же завтра
    need_day = datetime.datetime.today()
    need_day += datetime.timedelta(1)  # получаем завтрашний день
    if need_day.strftime('%A') == 'Sunday':
        need_day += datetime.timedelta(1)
    need_day = need_day.strftime('%A')
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT * FROM timetable WHERE school_id = "{}" '
                   'AND grade_id = "{}"'.format(school_id, grade_id))
    answer = list(cursor.fetchall()[0][2:])
    try:
        answer[0] = 'Понедельник:\n' + answer[0]
        answer[1] = 'Вторник:\n' + answer[1]
        answer[2] = 'Среда:\n' + answer[2]
        answer[3] = 'Четверг:\n' + answer[3]
        answer[4] = 'Пятница:\n' + answer[4]
        answer[5] = 'Суббота:\n' + answer[5]
    except TypeError:
        return 'Полного расписания нет.'
    else:
        answer = '\n'.join(answer)
        dict_of_days = {'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда',
                        'Thursday': 'Четверг', 'Friday': 'Пятница', 'Saturday': 'Суббота'}
        answer = answer[answer.find(dict_of_days.get(need_day)):]
        answer = answer[:answer.find('\n\n')]
        answer = get_homework(answer)    # дополняем расписание дзшкой
        answer += '\n\n'
        answer += get_birthday()
        return answer


def get_all_timetable():
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT * FROM timetable WHERE school_id = "{}" '
                   'AND grade_id = "{}"'.format(school_id, grade_id))
    answer = list(cursor.fetchall()[0][2:])
    try:
        answer[0] = 'Пн\n' + answer[0]
        answer[1] = 'Вт\n' + answer[1]
        answer[2] = 'Ср\n' + answer[2]
        answer[3] = 'Чт\n' + answer[3]
        answer[4] = 'Пт\n' + answer[4]
        answer[5] = 'Сб\n' + answer[5]
    except TypeError:
        return 'Полного расписания нет.'
    else:
        return '\n'.join(answer)


def get_desk():  # получение доски объявления выбранного класса
    school_id, grade_id = dict_of_data.get("school_id"), dict_of_data.get("grade_id")
    cursor.execute('SELECT * FROM grades WHERE grade_id = "{}" AND school_id = "{}"'.format(grade_id, school_id))
    result = cursor.fetchall()[0][6]
    if result == '-1':
        return 'Лента новостей пуста'
    return result


def get_afisha():  # получение афишы всей школы
    cursor.execute('SELECT * FROM schools WHERE school_id = "{}"'.format(dict_of_data.get("school_id")))
    return cursor.fetchall()[0][3]


def get_marks(id):
    if len(id) > 12:
        return None
    school_id, grade_id, stud_id = id[:3], id[3:6], id[6:]
    # получаем код ученика, школу, класс, его уч id
    cursor.execute('SELECT name_of_subject, mark FROM marks '
                   'WHERE school_id = "{}" AND grade_id = "{}" AND '
                   'stud_id = "{}"'.format(school_id, grade_id, stud_id))
    pre_marks = cursor.fetchall()
    # получение всех оценок заданного ученика
    if len(pre_marks) == 0:
        return None
    cursor.execute('SELECT name FROM students '
                   'WHERE school_id = "{}" AND grade_id = "{}" AND '
                   'stud_id = "{}"'.format(school_id, grade_id, stud_id))
    marks = 'Дневник ' + cursor.fetchall()[0][0] + ':\n'
    dict_of_temp = {}
    for i in pre_marks:     # делаем читабельную строку для нормального вывода
        if dict_of_temp.get(i[0]) is None:
            dict_of_temp.update({i[0]: i[1]})
        else:
            dict_of_temp[i[0]] += ', ' + i[1]
    for i in dict_of_temp.items():
        marks += i[0].capitalize() + ': ' + ','.join(i[1:]) + '\n'
    return marks


def print_hw():
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT subject, homework FROM homework WHERE school_id = "{}" AND'
                   ' grade_id = "{}"'.format(school_id, grade_id))  # находим нужное дз
    result = ''
    for i in cursor.fetchall():
        result += i[0].capitalize() + ': ' + i[1] + '\n'    # упорядачеваем дз, для норм вывода
    if len(result) == 0:
        return 'Домашнего задания нет.'
    else:
        return result


def check_teacher(login):
    cursor.execute('SELECT * FROM teachers WHERE '
                   'school_id = "{}" AND teacher_id = "{}"'.format(login[:3], login[3:]))
    if cursor.fetchall():
        dict_of_data['login'] = login
        dict_of_data['school_id'] = login[:3]   # записываем для сессии, чтоб препод не переписывал рум по 100 раз
        return False
    return True


def check_pass(password):
    login = dict_of_data.get('login')
    cursor.execute('SELECT * FROM teachers WHERE '
                   'school_id = "{}" AND teacher_id = "{}" AND '
                   'password = "{}"'.format(login[:3], login[3:], password))
    teacher = cursor.fetchall()
    if teacher:
        dict_of_data['password'] = password
        return True
    return None


def magazine():
    # функция на получение учеников по заданному предмету
    # + прибавление балов за вход в меню выставления оценок
    login, grade = dict_of_data.get('login'), dict_of_data.get('grade')
    cursor.execute('SELECT score FROM teachers WHERE school_id = "{}" AND teacher_id = "{}"'.format(login[:3], login[3:]))
    tmp = cursor.fetchall()[0][0]
    if tmp is None:
        tmp = 1
    else:
        tmp = str(int(tmp) + 1)
    cursor.execute('UPDATE teachers SET score = "{}" WHERE '
                   'school_id = "{}" AND teacher_id = "{}"'.format(tmp, login[:3], login[3:]))
    # прибавляем балл, за то что зашел в журнал
    conn.commit()
    cursor.execute('SELECT grade_id FROM grades WHERE '
                   'school_id = "{}" AND number_grade = "{}"'.format(login[:3], grade))
    grade_id = cursor.fetchall()
    if not grade_id:
        return []
    grade_id = dict_of_data['grade_id'] = grade_id[0][0]
    cursor.execute('SELECT name, stud_id FROM students '
                   'WHERE grade_id = "{}" AND school_id = "{}"'.format(grade_id, login[:3]))
    # получение списка всех студентов
    ls_of_result = []
    for i in cursor.fetchall():
        name_of_stud = i[0]
        name_of_stud = name_of_stud[:name_of_stud.find(' ') + 2] + '.'
        ls_of_result.append(i[1] + ':' + name_of_stud)
        dict_of_data['stud_id'].append(i[0])
        # выбираем учеников и их оценки по предмету
    return ls_of_result


def set_mark(mark):
    # установка оценки
    if not mark.isdigit():
        return False
    login, grade = dict_of_data.get('login'), dict_of_data.get('grade')
    cursor.execute('SELECT grade_id FROM grades '  # получаем айди класса, из его номера
                   'WHERE school_id = "{}" AND number_grade = "{}"'.format(login[:3], grade))
    stud_id = dict_of_data.get('last_stud_id')
    grade_id = cursor.fetchall()[0][0]
    if dict_of_data.get('subject') == '0':
        cursor.execute('SELECT name_of_subject FROM teachers '     # получаем предмет учителя
                       'WHERE school_id = "{}" AND teacher_id = "{}"'.format(login[:3], login[3:]))
        cursor.execute('INSERT INTO marks (school_id, grade_id, stud_id , name_of_subject , mark) '
                       'VALUES ("{}", "{}", "{}", "{}", "{}")'.format(login[:3], grade_id, stud_id, cursor.fetchall()[0][0], mark))
        # из полученных данных в инфо, выбираем предмет, айди студа и ставим в него оценку
        conn.commit()
    else:
        cursor.execute('INSERT INTO marks (school_id, grade_id, stud_id , name_of_subject , mark) '
                       'VALUES ("{}", "{}", "{}", "{}", "{}")'.format(login[:3], grade_id, stud_id,
                                                                      dict_of_data.get('subject'), mark))
    conn.commit()
    return True


def check_ad(id_ad):
    cursor.execute('SELECT name FROM res')
    for i in cursor.fetchall():
        if id_ad in i:
            dict_of_data['ad'] = id_ad
            return True
    else:
        return False


def change_ad(new_ad_text):
    # смена рекламы/банера, меняем
    new_ad_text = new_ad_text.replace('\\', '\\\\')
    name = dict_of_data.get('ad')
    cursor.execute('UPDATE res SET value = "{}" WHERE name = "{}"'.format(new_ad_text, name))
    conn.commit()


def set_tt(timetable, day):
    timetable += '\n'
    timetable = timetable.replace(';', '\n')
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    dict_of_days_rus = {'Пн': 'Mon', 'Вт': 'Tue', 'Ср': 'Wed',  # для внесения в бд нового расписания(по колонкам дни на англ)
                        'Чт': 'Thu', 'Пт': 'Fri', 'Сб': 'Sat'}
    cursor.execute('UPDATE timetable SET {} = "{}" '
                   'WHERE school_id = "{}" AND grade_id = "{}"'.format(dict_of_days_rus.get(day),
                                                                       timetable, school_id, grade_id))
    conn.commit()


def check_stud(all_id):
    school_id = dict_of_data['school_id'] = all_id[:3]
    grade_id = dict_of_data['grade_id'] = all_id[3:]
    cursor.execute('SELECT * FROM students WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    answer = cursor.fetchall()
    if len(answer) == 0:
        return None
    ls_of_result = []
    for i in answer:
        ls_of_result.append(i[2] + ':' + i[3])
    return ls_of_result


def delete_stud(stud_id):
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('DELETE FROM students WHERE stud_id = "{}" AND'
                   ' school_id = "{}" AND grade_id = "{}"'.format(stud_id, school_id, grade_id))
    cursor.execute('DELETE FROM marks WHERE stud_id = "{}" AND'
                   ' school_id = "{}" AND grade_id = "{}"'.format(stud_id, school_id, grade_id))
    # удаляем студента из таблицы с оценками и из общей таблицы
    conn.commit()


def change_id(stud_id):
    if len(stud_id) != 6:
        return False
    school_id = dict_of_data.get('school_id')
    grade_id = dict_of_data.get('grade_id')
    old_stud_id = dict_of_data.get('last_stud_id')[:6]  # режим от edit, так как пометка на инлайн
    cursor.execute('SELECT * FROM students WHERE stud_id = "{}" AND school_id = "{}" '
                   'AND grade_id = "{}"'.format(stud_id, school_id, grade_id))
    if cursor.fetchall():   # если id занят или ещё что-то не так
        return False
    print(stud_id, old_stud_id)
    cursor.execute('UPDATE students SET stud_id = "{}" WHERE stud_id = "{}" AND '
                   'school_id = "{}" AND grade_id = "{}"'.format(stud_id, old_stud_id, school_id, grade_id))
    cursor.execute('UPDATE marks SET stud_id = "{}" WHERE stud_id = "{}" AND '
                   'school_id = "{}" AND grade_id = "{}"'.format(stud_id, old_stud_id, school_id, grade_id))
    # обновляет студента, его айди, и следовательно его id для оценки
    conn.commit()
    return True


def check_teacher_id(all_id):
    cursor.execute('SELECT * FROM teachers WHERE school_id = "{}" AND '
                   'teacher_id = "{}"'.format(all_id[:3], all_id[3:]))
    return cursor.fetchall()


def new_teacher_schoold_id(new_id):
    if len(new_id) != 3:
        return False
    login = dict_of_data.get('login')
    cursor.execute('SELECT * FROM schools WHERE school_id = "{}"'.format(new_id))   # если нет школ с новым id
    if len(cursor.fetchall()) == 0:
        return
    cursor.execute('SELECT name_of_subject FROM teachers WHERE school_id = "{}"'  # взятие предмета учителя 
                   'AND teacher_id = "{}"'.format(login[:3], login[3:]))
    subject = cursor.fetchall()
    # print(subject)
    cursor.execute('SELECT * FROM teachers WHERE school_id = "{}"'   # проверка на одинаковый предмет
                   ' AND name_of_subject = "{}"'.format(new_id, subject[0][0]))
    if cursor.fetchall():
        return False
    cursor.execute('SELECT * FROM teachers WHERE school_id = "{}"'   # проверка на одинаковый учительский id
                   ' AND teacher_id = "{}"'.format(new_id, login[3:]))
    if cursor.fetchall():
        return False
    cursor.execute('UPDATE teachers SET school_id = "{}" WHERE school_id = "{}"'
                   ' AND teacher_id = "{}"'.format(new_id, login[:3], login[3:]))  # если всё удовлетворяет, меняем
    conn.commit()
    dict_of_data['login'] = new_id + dict_of_data.get('login')[3:]
    return True


def new_teacher_id(new_id):
    if len(new_id) != 4:
        return False
    login = dict_of_data.get('login')
    cursor.execute('SELECT * FROM teachers WHERE school_id = "{}" AND teacher_id = "{}"'.format(login[:3], new_id))  # проверяем нет ли уже занятого такого же id
    if cursor.fetchall():
        return False
    cursor.execute('UPDATE teachers SET teacher_id = "{}" WHERE teacher_id = "{}"'
                   ' AND school_id = "{}"'.format(new_id, login[3:], login[:3]))
    conn.commit()
    dict_of_data['login'] = dict_of_data.get('login')[:3] + new_id
    return True


def new_teacher_password(new_password):
    if len(new_password) > 32:
        return False
    login = dict_of_data.get('login')
    cursor.execute('UPDATE teachers SET password = "{}" WHERE teacher_id = "{}"'
                   ' AND school_id = "{}"'.format(new_password, login[3:], login[:3]))
    conn.commit()
    return True


def new_teacher_subj(subj):
    if len(subj) > 31:
        return False
    login = dict_of_data.get('login')
    cursor.execute('SELECT name_of_subject FROM teachers '
                   'WHERE name_of_subject = "{}" AND school_id = "{}"'.format(subj, login[:3]))
    # проверяем нет ли такого же учителя уже, если есть, запрещаем создавать клона
    if cursor.fetchall():
        return False
    cursor.execute('UPDATE teachers SET name_of_subject = "{}" WHERE teacher_id = "{}"'
                   ' AND school_id = "{}"'.format(subj, login[3:], login[:3]))
    conn.commit()
    return True


def delete_teacher():
    login = dict_of_data.get('login')
    cursor.execute('DELETE FROM teachers WHERE teacher_id = "{}" AND school_id = "{}"'.format(login[3:], login[:3]))
    conn.commit()


def grades():
    login = dict_of_data.get('login')
    cursor.execute('SELECT number_grade FROM grades WHERE school_id = "{}"'.format(login[:3]))
    return cursor.fetchall()


def change_homework_for_class(homework):
    login, grade = dict_of_data.get('login'), dict_of_data.get('grade')
    cursor.execute('SELECT score FROM teachers WHERE school_id = "{}" AND '
                   'teacher_id = "{}"'.format(login[:3],
                                              login[3:]))  # + прибавление балов за вход в меню выставления оценок
    tmp = cursor.fetchall()[0][0]
    if tmp is None:
        tmp = 3
    else:
        tmp = str(int(tmp) + 3)
    cursor.execute('UPDATE teachers SET score = "{}" WHERE '
                   'school_id = "{}" AND teacher_id = "{}"'.format(tmp, login[:3], login[3:]))
    conn.commit()

    cursor.execute('SELECT grade_id FROM grades WHERE school_id = "{}"'   # получаем класс, который хотел редактировать учитель
                   ' AND number_grade = "{}"'.format(login[:3], grade))
    grade_id = cursor.fetchall()
    if len(grade_id) == 0:
        return 'Такого класса не существует.\nПопробуйте заного(/room)'
    else:
        grade_id = grade_id[0][0]


    cursor.execute('SELECT * FROM homework WHERE school_id = "{}" '
                   'AND grade_id = "{}" AND subject = "{}"'.format(login[:3], grade_id, dict_of_data.get('subject')))

    if cursor.fetchall():
        cursor.execute('UPDATE homework SET homework = "{}" WHERE school_id = "{}" '
                       'AND grade_id = "{}" AND subject = "{}"'.format(homework, login[:3], grade_id, dict_of_data.get('subject')))
    else:
        cursor.execute('INSERT INTO homework (school_id, grade_id, subject, homework)'
                       ' VALUES ("{}", "{}", "{}", "{}")'.format(login[:3], grade_id, dict_of_data.get('subject'), homework))
    conn.commit()
    return 'Новое домашнее задание по предмету : {}:\n{}'.format(dict_of_data.get('subject'), homework)


def change_homework(homework):  # функция на изменение домашки

    login, grade = dict_of_data.get('login'), dict_of_data.get('grade')
    cursor.execute('SELECT score FROM teachers WHERE school_id = "{}" AND '
                   'teacher_id = "{}"'.format(login[:3], login[3:]))    # + прибавление балов за вход в меню выставления оценок
    tmp = cursor.fetchall()[0][0]
    if tmp is None:
        tmp = 3
    else:
        tmp = str(int(tmp) + 3)
    cursor.execute('UPDATE teachers SET score = "{}" WHERE '
                   'school_id = "{}" AND teacher_id = "{}"'.format(tmp, login[:3], login[3:]))
    conn.commit()

    cursor.execute('SELECT name_of_subject FROM teachers WHERE teacher_id = "{}"'  # получаем из id предмет учителя
                   ' AND school_id = "{}"'.format(login[3:], login[:3]))

    subject = cursor.fetchall()[0][0]
    cursor.execute('SELECT grade_id FROM grades WHERE school_id = "{}"'   # получаем класс, который хотел редактировать учитель
                   ' AND number_grade = "{}"'.format(login[:3], grade))

    grade_id = cursor.fetchall()
    if len(grade_id) == 0:
        return 'Такого класса не существует.\nПопробуйте заного(/room)'
    else:
        grade_id = grade_id[0][0]

    cursor.execute('SELECT * FROM homework WHERE school_id = "{}" AND '   # запрос на проверку, есть ли вообще дз, если нет добавляем иначе, редачим
                   'grade_id = "{}" AND subject = "{}"'.format(login[:3], grade_id, subject))

    if len(cursor.fetchall()) == 0:
        cursor.execute('INSERT INTO homework (school_id, grade_id, subject, homework) '     # добавление в таблицу нового дз на класс
                       'VALUES ("{}", "{}", "{}", "{}")'.format(login[:3], grade_id, subject, homework))
    else:
        cursor.execute('UPDATE homework SET homework.homework = "{}" '  # обнговление дз в таблице
                       'WHERE grade_id = "{}" AND school_id = "{}" AND subject = "{}"'.format(homework, grade_id, login[:3], subject))
    conn.commit()   # редактируем дз класса и комитим

    cursor.execute('SELECT homework FROM homework WHERE '      # выводим на экран. чтоб он мног проверить
                   'grade_id = "{}" AND school_id = "{}" AND subject = "{}"'.format(grade_id, login[:3], subject))
    result = cursor.fetchall()
    if result:
        return result[0][0]
    else:
        return 'Задание не удалось обновить.\nПопробуйте заного(/room)'


def check_grade():
    grade, school_id = dict_of_data.get('grade'), dict_of_data.get('login')[:3]
    cursor.execute('SELECT * FROM grades WHERE '
                   'number_grade = "{}" AND school_id = "{}"'.format(grade, school_id))
    if cursor.fetchall():
        return False
    return True


def create_school(id_new_school):   #  создание новой шк в базе данных
    if len(id_new_school) != 3:
        return False

    cursor.execute('SELECT * FROM schools WHERE school_id = "{}"'.format(id_new_school))    # проверяет если id уже занят
    if cursor.fetchall():
        return False

    new_school = 'Новосозданная школа'  # все поля с этой переменной будут позже редачится админом
    cursor.execute('INSERT INTO schools (name_school, slogan, school_id, news_of_school) '
                   'VALUES ("{}", "{}", "{}", "{}")'.format(new_school, new_school, id_new_school, new_school))
    conn.commit()   # заводим новую шк в бд
    dict_of_data['school_id'] = id_new_school
    return True


def set_title_of_school(title):
    if len(title) > 63:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute('SELECT * FROM schools WHERE name_school = "{}"'.format(title))  # проверяем нет ли у кого такого же названия
    if cursor.fetchall():
        return False
    cursor.execute('UPDATE schools SET name_school = "{}" WHERE school_id = "{}"'.format(title, school_id))
    conn.commit()
    return True


def set_new_afisha(afisha):
    if len(afisha) > 511:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute('SELECT * FROM schools WHERE school_id = "{}"'.format(school_id))
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute('UPDATE schools SET news_of_school = "{}" WHERE school_id = "{}"'.format(afisha, school_id))
    conn.commit()
    return True


def check_school(school_id):
    cursor.execute('SELECT * FROM schools WHERE school_id = "{}"'.format(school_id))
    if cursor.fetchall():
        dict_of_data['school_id'] = school_id   # проверка введенной школы + занос в словарь
        return True
    else:
        return False


def create_grade(grade_id):
    if len(grade_id) != 3:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute('SELECT * FROM grades WHERE grade_id = "{}" AND school_id = "{}"'.format(grade_id, school_id))
    if len(cursor.fetchall()) != 0:
        return False
    school_id = dict_of_data.get('school_id')
    new_grade = 'Новый класс'
    # вводим новый класс в бд, поля new_grade позже буду заполненным инфой от админа
    cursor.execute('INSERT INTO grades (school_id, number_grade, grade_id, '
                   'photo_teacher, name_of_teacher, invite_url, bulletin_board) '
                   'VALUES ("{}", "new", "{}", "{}", "{}", -1, "{}")'.format(school_id, grade_id, new_grade, new_grade, new_grade))
    conn.commit()
    dict_of_data['grade_id'] = grade_id
    # так добавляем класс в расписания таблицу, чтоб в него давать раписания класса
    cursor.execute('INSERT INTO timetable (school_id, grade_id) VALUES'
                   ' ("{}", "{}")'.format(school_id, grade_id))
    conn.commit()
    return True


def set_number(number):
    if len(number) > 7:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT * FROM grades WHERE school_id = "{}" '
                   'AND grade_id = "{}"'.format(school_id, grade_id))     # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute('SELECT * FROM grades WHERE school_id = "{}" '
                   'AND number_grade = "{}"'.format(school_id, number))   # проверяем нет ли уже такого номера в шк
    if cursor.fetchall():
        return False
    cursor.execute('UPDATE grades SET number_grade = "{}" WHERE school_id = "{}" AND '
                   'grade_id = "{}"'.format(number, school_id, grade_id))
    conn.commit()
    return True


def set_photo(photo):
    if len(photo) > 127:
        return False
    photo = photo.replace('\\', '\\\\')
    try:
        open(photo, 'rb')
    except:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        'SELECT * FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute('UPDATE grades SET photo_teacher = "{}" WHERE school_id = "{}" AND '
                   'grade_id = "{}"'.format(photo, school_id, grade_id))
    conn.commit()
    return True


def set_grade_name_teacher(name_of_teacher):
    if len(name_of_teacher) > 63:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        'SELECT * FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(
        'UPDATE grades SET name_of_teacher = "{}" WHERE school_id = "{}" AND '
        'grade_id = "{}"'.format(name_of_teacher, school_id, grade_id))
    conn.commit()
    return True


def set_code(code):
    if len(code) > 45:
        return False
    elif code.find('https://t.me/joinchat/') == -1 and code.find('https://t.me/') == -1:
        if code != '-1':
            return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        'SELECT * FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(
        'UPDATE grades SET invite_url = "{}" WHERE school_id = "{}" AND grade_id = "{}"'.format(code, school_id, grade_id))
    conn.commit()
    return True


def set_desk(text):
    if len(text) > 1023:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        'SELECT * FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False

    # махинация для добавления новости, и удалений старых
    cursor.execute('SELECT bulletin_board FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    news = cursor.fetchall()[0][0]
    if news.find('Новая доска') == 0:
        news = text
    else:
        news += '\n\n\n' + text
        while len(news) > 1023:
            news = news[news.find('\n\n\n'):]   # режем старые, если кончилось место
    if text == '-1':
        news = 'Доска объявлений пуста.'
    cursor.execute(
        'UPDATE grades SET bulletin_board = "{}" WHERE school_id = "{}" AND grade_id = "{}"'.format(news, school_id, grade_id))
    conn.commit()
    return True


def create_stud(name):
    if len(name) > 31:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT * FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))  # проверяем классы
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute('INSERT INTO students (school_id, grade_id, name, stud_id) VALUES '  # заносим в таблицу
                   '("{}", "{}", "{}", "-1")'.format(school_id, grade_id, name))
    conn.commit()
    dict_of_data['name'] = name
    return True


def set_stud_id(id):
    if len(id) != 6:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        'SELECT * FROM students WHERE school_id = "{}" AND grade_id = "{}" '
        'AND stud_id = "{}"'.format(school_id, grade_id, id))  # проверяем классы на клона, то есть чтоб не было такого же id
    if len(cursor.fetchall()) != 0:
        return False
    name = dict_of_data.get('name')
    cursor.execute('UPDATE students SET stud_id = "{}" WHERE school_id = "{}" AND grade_id = "{}" '
                   'AND name = "{}"'.format(id, school_id, grade_id, name))
    conn.commit()
    return True


def get_school(school_id):
    if len(school_id) > 3:
        return False
    cursor.execute('SELECT * FROM schools WHERE school_id = "{}"'.format(school_id))    # проверяем школу
    if len(cursor.fetchall()) == 0:
        return False
    dict_of_data['school_id'] = school_id
    return True


def create_teach(teacher_id):
    if len(teacher_id) > 4:
        return False
    new_teacher, school_id = '-1', dict_of_data.get('school_id')
    cursor.execute('SELECT * FROM teachers WHERE school_id = "{}" AND teacher_id = "{}"'.format(school_id, teacher_id))   # если есть уже с такими id
    if len(cursor.fetchall()) != 0:
        return False
    # добавляем в бд, и потом редачим его
    cursor.execute('INSERT INTO teachers (school_id , teacher_id, password, name_of_subject, score) VALUES '
                   '("{}", "{}", password = "-1", name_of_subject = "-1", score = "{}" )'.format(school_id, teacher_id, str(0)))
    conn.commit()
    dict_of_data['login'] = school_id + teacher_id
    return True


def set_name_of_school(name):
    if len(name) > 63:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute('UPDATE schools SET name_school = "{}" WHERE school_id = "{}"'.format(name, school_id))
    conn.commit()
    return True


def set_news(news):
    if len(news) > 511:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute('SELECT news_of_school FROM schools WHERE school_id = "{}"'.format(school_id))   # для добавления новой новости
    old_news = cursor.fetchall()[0][0]
    old_news += '\n\n\n' + news
    while len(old_news) > 511:   # если новостей уже много, режем пстарые новости
        old_news = old_news[old_news.find('\n\n\n') + 3:]
    cursor.execute('UPDATE schools SET news_of_school = "{}" WHERE school_id = "{}"'.format(old_news, school_id))
    conn.commit()
    return True


def get_ad():   # возвращаем всю рекламку
    cursor.execute('SELECT * FROM res')
    return cursor.fetchall()


def get_invite_url():   # возвращаем ссылку приглос
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT invite_url FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    url = cursor.fetchall()[0][0]
    if url == '-1':
        return 'Ссылки-приглашения не существует.'
    return url


def delete_school():
    school_id = dict_of_data.get('school_id')
    cursor.execute('DELETE FROM schools WHERE school_id = "{}"'.format(school_id))
    conn.commit()
    cursor.execute('DELETE FROM grades WHERE school_id = "{}"'.format(school_id))
    conn.commit()
    cursor.execute('DELETE FROM students WHERE school_id = "{}"'.format(school_id))
    conn.commit()
    cursor.execute('DELETE FROM timetable WHERE school_id = "{}"'.format(school_id))
    conn.commit()
    cursor.execute('DELETE FROM homework WHERE school_id = "{}"'.format(school_id))
    conn.commit()
    cursor.execute('DELETE FROM marks WHERE school_id = "{}"'.format(school_id))
    conn.commit()


def delete_grade():
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('DELETE FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    conn.commit()
    cursor.execute('DELETE FROM marks WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    conn.commit()
    cursor.execute('DELETE FROM students WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    conn.commit()
    cursor.execute('DELETE FROM timetable WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    conn.commit()
    cursor.execute('DELETE FROM homework WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    conn.commit()


def import_stud(new_students):
    failure_result = ''
    while new_students.find(', ') > -1: # цикл бежит по строкам
        school_id = new_students[:new_students.find(', ')]  # получаем скул id
        new_students = new_students[new_students.find(', ') + 2:]
        grade_id = new_students[:new_students.find(', ')]   # получаем грейд id
        new_students = new_students[new_students.find(', ') + 2:]
        name = new_students[:new_students.find(', ')]   # получаем имя
        new_students = new_students[new_students.find(', ') + 2:]
        # тут сравниваем, админ может быть криворучка, и ввести нечайно лишний энтер в конце файл
        if new_students.find('\n') > -1:    # если не конец файла
            stud_id = new_students[:new_students.find('\n') - 1]
            new_students = new_students[new_students.find('\n') + 1:]
        else:   # если конец файла
            stud_id = new_students
        # print(school_id, grade_id, name, stud_id) # принт значений из файла
        # print(len(school_id), len(grade_id), len(name), len(stud_id)) # принт их длины(для проверки)
        if len(school_id) != 3 or len(grade_id) != 3 or len(name) > 31 or len(stud_id) != 3:    # если не по форме ученик
            failure_result += 'Ученик не ипортирован - ' + school_id + ' ' + grade_id + ' ' \
                              + name + ' ' + stud_id + ' -- так как ученик введен не по форме;\n'
            continue

        cursor.execute('SELECT * FROM students WHERE school_id = "{}" AND grade_id = "{}" '     # проверяем есть ли такой уже в базе
                       'AND stud_id = "{}"'.format(school_id, grade_id, stud_id))

        if cursor.fetchall():   # если такой в базе есть, выкидываем ошибку
            failure_result += 'Ученик не ипортирован - ' + school_id + ' ' + grade_id + ' ' + name \
                              + ' ' + stud_id + ' -- данный ученик уже есть в базе;\n'
            continue
        else:
            failure_result += 'Ученик ИМПОРТИРОВАН - ' + school_id + ' ' + grade_id + ' ' + name \
                              + ' ' + stud_id + '\n'

        cursor.execute('INSERT INTO students (school_id, grade_id, name, stud_id) VALUES '
                       '("{}", "{}", "{}", "{}")'.format(school_id, grade_id, name, stud_id))
        conn.commit()
    return failure_result


def import_teach(new_teachers):
    # print(new_teachers)
    failure_result = ''
    while new_teachers.find(', ') > -1:  # цикл бежит по строкам
        school_id = new_teachers[:new_teachers.find(', ')]
        new_teachers = new_teachers[new_teachers.find(', ') + 2:]
        teacher_id = new_teachers[:new_teachers.find(', ')]
        new_teachers = new_teachers[new_teachers.find(', ') + 2:]
        password = new_teachers[:new_teachers.find(', ')]
        new_teachers = new_teachers[new_teachers.find(', ') + 2:]
        subject = new_teachers[:new_teachers.find(', ')]
        new_teachers = new_teachers[new_teachers.find(', ') + 2:]
        # тут сравниваем, админ может быть криворучка, и ввести нечайно лишний энтер в конце файл
        if new_teachers.find('\n') > -1:  # если не конец файла
            score = new_teachers[:new_teachers.find('\n') - 1]
            new_teachers = new_teachers[new_teachers.find('\n') + 1:]
        else:  # если конец файла
            # print(new_teachers)
            score = new_teachers

        data_of_teacher = school_id + ' ' + teacher_id + ' ' + password + ' ' + subject + ' ' + score   # для уменьшения кол-ва кода

        # print(data_of_teacher)
        # print(len(school_id), len(teacher_id), len(password), len(subject), len(score))

        if len(school_id) != 3 or len(teacher_id) > 4 or len(password) > 32 or len(subject) > 31 or len(score) > 9:  # если не по форме ученик
            failure_result += 'Учитель не ипортирован - ' + data_of_teacher\
                              + ' -- так как учитель введен не по форме;\n'
            continue

        cursor.execute(
            'SELECT * FROM teachers WHERE school_id = "{}" AND teacher_id = "{}" '.format(school_id, teacher_id))  # проверяем есть ли такой уже в базе

        if cursor.fetchall():
            failure_result += 'Учитель не ипортирован - ' + data_of_teacher\
                              + ' -- учитель с идентичными ID уже есть в базе;\n'
            continue

        cursor.execute('SELECT * FROM teachers WHERE school_id = "{}" AND name_of_subject = "{}"'.format(school_id, subject))

        if cursor.fetchall():  # если такой в базе есть, выкидываем ошибку
            failure_result += 'Учитель не ипортирован - ' + data_of_teacher\
                              + ' -- данный учитель не подходит по предмету в данную школу;\n'
            continue
        else:
            failure_result += 'Учитель ИМПОРТИРОВАН - ' + data_of_teacher + '\n'

        cursor.execute('INSERT INTO teachers (school_id, teacher_id, password, name_of_subject, score) VALUES '
                       '("{}", "{}", "{}", "{}", "{}")'.format(school_id, teacher_id, password, subject, score))
        conn.commit()
    return failure_result


def import_timetable(new_timetable):
    failure_result = ''
    while new_timetable.find(', ') > -1:  # цикл бежит по строкам
        school_id = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        grade_id = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        mon = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        tue = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        wed = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        thu = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        fri = new_timetable[:new_timetable.find(', ')]
        new_timetable = new_timetable[new_timetable.find(', ') + 2:]
        if new_timetable.find('\n') > -1:  # если не конец файла
            sat = new_timetable[:new_timetable.find('\n') - 1]
            new_timetable = new_timetable[new_timetable.find('\n') + 1:]
        else:  # если конец файла
            # print(new_teachers)
            sat = new_timetable

        data_of_timetable = school_id + " " + grade_id + " " + mon + " " + tue + " " + wed + " " + thu + " " + fri + " " + sat
        # делаем отступы + приводим в порядок
        mon = mon.replace(';', '\n') + '\n'
        tue = tue.replace(';', '\n') + '\n'
        wed = wed.replace(';', '\n') + '\n'
        thu = thu.replace(';', '\n') + '\n'
        fri = fri.replace(';', '\n') + '\n'
        sat = sat.replace(';', '\n') + '\n'

        if len(school_id) != 3 or len(grade_id) != 3 or len(mon) > 127 or len(tue) > 127 or len(wed) > 127 or len(thu) > 127 or len(fri) > 127 or len(sat) > 127:
            failure_result += 'Расписание - ' + data_of_timetable + ' -- не импортировано ' \
                                                                    'так как написано не в том формате;\n'
            continue
        if len(mon) < 1 or len(tue) < 1 or len(wed) < 1 or len(thu) < 1 or len(fri) < 1 or len(sat) < 1:
            failure_result += 'Расписание - ' + data_of_timetable + ' -- не импортировано ' \
                                                                    'так как написано не в том формате;\n'
            continue

        cursor.execute('SELECT * FROM timetable WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))

        print(data_of_timetable)
        if cursor.fetchall():   # если класс уже был в бд
            failure_result += 'Расписание - ' + data_of_timetable + ' -- ИМПОРТИРОВАНО ' \
                                                                    'и ОБНОВЛЕННО;\n'
            cursor.execute('UPDATE timetable SET mon = "{}", tue = "{}", wed = "{}", thu = "{}", '
                           'fri = "{}", sat = "{}" WHERE school_id = "{}" AND '
                           'grade_id = "{}"'.format(mon, tue, wed, thu, fri, sat, school_id, grade_id))
            conn.commit()
        else:
            failure_result += 'Расписание - ' + data_of_timetable + ' -- ИМПОРТИРОВАНО успешно.\n'
            cursor.execute('INSERT INTO timetable (school_id, grade_id, mon, tue, wed, thu, fri, sat) '
                           'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(school_id, grade_id, mon, tue, wed, thu, fri, sat))
            conn.commit()

    return failure_result


def export_students():
    cursor.execute('SELECT * FROM students')
    result = cursor.fetchall()
    if result:
        temp_ls = []  # для помещения туда одного ученика
        all_temp_ls = []  # для помещения туда всех учеников
        for i in result:
            for j in i:
                temp_ls.append(j)
            all_temp_ls.append(temp_ls)
            temp_ls = []
        result = tabulate(all_temp_ls, headers=['school_id', 'grade_id', 'name', 'stud_id'])    # делаем красивую табличку,
    else:
        result = 'Нет учеников'   # если учеников нет, так и пишем
    with open('temp_file.txt', "w") as f:
        f.write(result)


def export_teachers():
    cursor.execute('SELECT * FROM teachers')
    result = cursor.fetchall()
    if result:
        temp_ls = []  # для помещения туда одного ученика
        all_temp_ls = []  # для помещения туда всех учеников
        for i in result:
            for j in i:
                temp_ls.append(j)
            all_temp_ls.append(temp_ls)
            temp_ls = []
        result = tabulate(all_temp_ls, headers=['school_id', 'teacher_id', 'password', 'subject', 'score'])    # делаем красивую табличку,
    else:
        result = 'Нет учителей'   # если учеников нет, так и пишем
    with open('temp_file.txt', "w") as f:
        f.write(result)


def get_grade_marks():  # получение оценок класса заданного преподователем
    login, school_id, grade_id = dict_of_data.get('login'), dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT * FROM marks WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))    # пробиваем оценки
    list_of_marks = cursor.fetchall()
    list_of_students = set()    # делаем множество учеников, для вывода учеников + оценок
    for i in list_of_marks:
        cursor.execute('SELECT * FROM students WHERE school_id = "{}" AND grade_id = "{}"'
                       'AND stud_id = "{}"'.format(school_id, grade_id, i[2]))
        list_of_students.add(cursor.fetchall()[0])
    cursor.execute('SELECT number_grade FROM grades WHERE school_id = "{}" AND grade_id = "{}"'.format(school_id, grade_id))
    result = 'Класс - ' + cursor.fetchall()[0][0]
    subject = dict_of_data.get('subject')
    if dict_of_data.get('subject') == '0' and login.find('к') == -1:
        cursor.execute('SELECT name_of_subject FROM teachers WHERE school_id = "{}" AND teacher_id = "{}"'.format(school_id, dict_of_data.get('login')[3:]))    # получаем предмет учителя
        subject = cursor.fetchall()[0][0]
    for i in list_of_students:
        result += '\n' + i[2] + ' : '
        for j in list_of_marks:
            if j[2] == i[3] and j[3] == subject:
                result += j[4] + ' '

    if len(result) == 0:
        return 'Оценок ещё нет.'
    else:
        return result


def check_classroom_teacher():      # установка дз классного руководителя
    login = dict_of_data.get('login')
    if login.find('к') == -1:
        return False
    cursor.execute('SELECT name_of_subject FROM teachers WHERE school_id = "{}" AND teacher_id = "{}"'.format(login[:3], login[3:]))
    whoisit = cursor.fetchall()[0][0]   # получаем предмет кл руководителя, который он хочет выставить
    if whoisit.find('к') == -1:    # код классного преподователя к10a
        return False
    dict_of_data['grade'] = whoisit[1:] # записываем класс классного руководителя
    return True


if __name__ == '__main__':
    pass
