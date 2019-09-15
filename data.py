import mysql.connector
import requests
import datetime

TOKEN = '914271777:AAGrCkpUMSUKOeg0VOh06eyz-XF-gXxQa34'

conn = mysql.connector.connect(user='root', password='0000001', host='127.0.0.1', database='tgbot')
cursor = conn.cursor(buffered=True)

dict_of_data = {'login': '0', 'password': '0', 'grade': '0',
                'school_id': '0', 'grade_id': '0', 'name': '0'}   # словарь с аудентификаторными данными
cancel_word = 'отмена'
dict_of_admins = {704369002: "1",
                  }


def get_res(text):   # для получения рекламы
    cursor.execute(f'SELECT * FROM res')
    for i in cursor.fetchall():
        if text == i[0]:
            return i[1]


def get_list_of_schools():  # получение всех школ участвующих в проекте
    cursor.execute(f'SELECT name_school FROM schools')
    result_str = ''
    for i in cursor.fetchall():
        result_str += i[0] + '\n'
    return result_str


def get_grade(id):    # получение инфы о одном каком-либо классе
    if len(id) != 6:    # если не по форме сразу выкидыш
        return None
    school_id, grade_id = id[:3], id[3:]
    cursor.execute(f'SELECT * FROM schools, grades '
                   f'WHERE schools.school_id = "{school_id}" AND grades.grade_id = "{grade_id}"')
    # узнаем есть ли класс в проекте
    answer = cursor.fetchall()
    if len(answer) == 0:  # если класс введен неверно, выходим
        return None
    cursor.execute(f'SELECT * FROM grades WHERE grade_id = {grade_id}')  # получаем нужный класс
    ls_of_result = []   # создаем список, чтоб пихать туда весь собранный резуль, а именно:
    # расписание, учеников
    answer = cursor.fetchall()
    ls_of_result.append(answer[0])
    cursor.execute(f'SELECT * FROM timetable WHERE school_id = "{school_id}" '
                   f'AND grade_id = "{grade_id}"')
    answer = list(cursor.fetchall()[0][2:])
    try:
        answer[0] = 'Понедельник:\n' + answer[0]
        answer[1] = 'Вторник:\n' + answer[1]
        answer[2] = 'Среда:\n' + answer[2]
        answer[3] = 'Четверг:\n' + answer[3]
        answer[4] = 'Пятница:\n' + answer[4]
        answer[5] = 'Суббота:\n' + answer[5]
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


def get_timetable_on_tomorrow():
    # получение расписание на след. день, или же завтра
    need_day = datetime.datetime.today()
    need_day += datetime.timedelta(1)  # получаем завтрашний день
    if need_day.strftime('%A') == 'Sunday':
        need_day += datetime.timedelta(1)
    need_day = need_day.strftime('%A')
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(f'SELECT * FROM timetable WHERE school_id = "{school_id}" '
                   f'AND grade_id = "{grade_id}"')
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
        return answer


def get_all_timetable():
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(f'SELECT * FROM timetable WHERE school_id = "{school_id}" '
                   f'AND grade_id = "{grade_id}"')
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
        return '\n'.join(answer)


def get_desk():  # получение доски объявления выбранного класса
    cursor.execute(f'SELECT * FROM grades WHERE grade_id = {dict_of_data.get("grade_id")}')
    return cursor.fetchall()[0][6]


def get_afisha():  # получение афишы всей школы
    cursor.execute(f'SELECT * FROM schools WHERE school_id = {dict_of_data.get("school_id")}')
    return cursor.fetchall()[0][3]


def get_marks(id):
    if len(id) > 9:
        return None
    school_id, grade_id, stud_id = id[:3], id[3:6], id[6:]
    # получаем код ученика, школу, класс, его уч id
    cursor.execute(f'SELECT name_of_subject, mark FROM marks '
                   f'WHERE school_id = "{school_id}" AND grade_id = "{grade_id}" AND '
                   f'stud_id = {stud_id}')
    pre_marks = cursor.fetchall()
    # получение всех оценок заданного ученика
    if len(pre_marks) == 0:
        return None
    marks = ''
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
    cursor.execute(f'SELECT subject, homework FROM homework WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"') # находим нужное дз
    result = ''
    for i in cursor.fetchall():
        result += i[0].capitalize() + ': ' + i[1] + '\n'    # упорядачеваем дз, для норм вывода
    if len(result) == 0:
        return 'Домашнего задания нет.'
    else:
        return result


def check_teacher(login):
    cursor.execute(f'SELECT * FROM teachers WHERE '
                   f'school_id = "{login[:3]}" AND teacher_id = "{login[3:]}"')
    if cursor.fetchall():
        dict_of_data['login'] = login
        return False
    return True


def check_pass(password):
    login = dict_of_data.get('login')
    cursor.execute(f'SELECT * FROM teachers WHERE '
                   f'school_id = "{login[:3]}" AND teacher_id = "{login[3:]}" AND '
                   f'password = "{password}"')
    teacher = cursor.fetchall()
    if teacher:
        dict_of_data['password'] = password
        return True
    return None


def magazine():
    # функция на получение учеников по заданному предмету
    # + прибавление балов за вход в меню выставления оценок
    login, password, grade = dict_of_data.get('login'), dict_of_data.get('password'), dict_of_data.get('grade')
    cursor.execute(f'SELECT score FROM teachers WHERE school_id = "{login[:3]}" AND teacher_id = "{login[3:]}"')
    tmp = cursor.fetchall()[0][0]
    if tmp is None:
        tmp = 1
    else:
        tmp = str(int(tmp) + 1)
    cursor.execute(f'UPDATE teachers SET score = "{tmp}" WHERE '
                   f'school_id = "{login[:3]}" AND teacher_id = "{login[3:]}"')
    # прибавляем балл, за то что зашел в журнал
    conn.commit()
    cursor.execute(f'SELECT grade_id FROM grades WHERE '
                   f'school_id = "{login[:3]}" AND number_grade = "{grade}"')
    cursor.execute(f'SELECT name, stud_id FROM students '
                   f'WHERE grade_id = "{cursor.fetchall()[0][0]}" AND school_id = "{login[:3]}"')
    # получение списка всех студентов
    ls_of_result = []
    for i in cursor.fetchall():
        ls_of_result.append(i[1] + ':' + i[0])
        # выбираем учеников и их оценки по предмету
    return ls_of_result


def set_mark(mark, stud_id):
    # установка оценки
    login, grade = dict_of_data.get('login'), dict_of_data.get('grade')
    cursor.execute(f'SELECT grade_id FROM grades '  # получаем айди класса, из его номера
                   f'WHERE school_id = "{login[:3]}" AND number_grade = "{grade}"')
    grade_id = cursor.fetchall()[0][0]
    cursor.execute(f'SELECT name_of_subject FROM teachers '     # получаем предмет учителя
                   f'WHERE school_id = "{login[:3]}" AND teacher_id = "{login[3:]}"')
    cursor.execute(f'INSERT INTO marks (school_id, grade_id, stud_id , name_of_subject , mark) '
                   f'VALUES ("{login[:3]}", "{grade_id}", "{stud_id}", "{cursor.fetchall()[0][0]}", "{mark}")')
    # из полученных данных в инфо, выбираем предмет, айди студа и ставим в него оценку
    conn.commit()


def check_ad(type_ad, number_ad):
    if type_ad == 'текст':
        dict_of_ad = {'1': 'first_ad', '2': 'second_ad'}
        cursor.execute(f'SELECT value FROM res WHERE name = "{dict_of_ad.get(number_ad)}"')
        if cursor.fetchall():
            return False
        return True
    else:
        dict_of_ad = {'1': 'first_pic', '2': 'second_pic'}
        cursor.execute(f'SELECT value FROM res WHERE name = "{dict_of_ad.get(number_ad)}"')
        if cursor.fetchall():
            return False
        return True


def change_ad(type_ad, number_ad, new_res):
    # смена рекламы/банера, меняем
    if type_ad == 'текст':
        dict_of_ad = {'1': 'first_ad', '2': 'second_ad'}
        cursor.execute(f'UPDATE res SET value = "{new_res}" '
                       f'WHERE name = "{dict_of_ad.get(number_ad)}"')
        conn.commit()
    else:
        dict_of_ad = {'1': 'first_pic', '2': 'second_pic'}
        cursor.execute(f'UPDATE res SET value = "{new_res}" '
                       f'WHERE name = "{dict_of_ad.get(number_ad)}"')
        conn.commit()


def set_tt(timetable, day):
    timetable += '\n'
    timetable = timetable.replace(';', '\n')
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    dict_of_days_rus = {'Понедельник': 'Mon', 'Вторник': 'Tue', 'Среда': 'Wed',  # для внесения в бд нового расписания(по колонкам дни на англ)
                        'Четверг': 'Thu', 'Пятница': 'Fri', 'Суббота': 'Sat'}
    cursor.execute(f'UPDATE timetable SET {dict_of_days_rus.get(day)} = "{timetable}" '
                   f'WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    conn.commit()


def check_stud(all_id):
    school_id = dict_of_data['school_id'] = all_id[:3]
    grade_id = dict_of_data['grade_id'] = all_id[3:]
    cursor.execute(f'SELECT * FROM students WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    answer = cursor.fetchall()
    if len(answer) == 0:
        return None
    ls_of_result = []
    for i in answer:
        ls_of_result.append(i[2] + ':' + i[3])
    return ls_of_result


def delete_stud(stud_id):
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(f'DELETE FROM students WHERE stud_id = "{stud_id}" AND school_id = "{school_id}" AND grade_id = "{grade_id}"')
    cursor.execute(f'DELETE FROM marks WHERE stud_id = "{stud_id}" AND school_id = "{school_id}" AND grade_id = "{grade_id}"')
    # удаляем студента из таблицы с оценками и из общей таблицы
    conn.commit()


def change_id(stud_id, old_stud_id):
    if len(stud_id) != 3:
        return False
    school_id = dict_of_data.get('school_id')
    grade_id = dict_of_data.get('grade_id')
    cursor.execute(f'SELECT * FROM students WHERE stud_id = "{stud_id}" AND school_id = "{school_id}" '
                   f'AND grade_id = "{grade_id}"')
    if cursor.fetchall():   # если id занят или ещё что-то не так
        return False
    cursor.execute(f'UPDATE students SET stud_id = "{stud_id}" WHERE stud_id = "{old_stud_id}" AND '
                   f'school_id = "{school_id}" AND grade_id = "{grade_id}"')
    cursor.execute(f'UPDATE marks SET stud_id = "{stud_id}" WHERE stud_id = "{old_stud_id}" AND '
                   f'school_id = "{school_id}" AND grade_id = "{grade_id}"')
    # обновляет студента, его айди, и следовательно его id для оценки
    conn.commit()
    return True


def check_teacher_id(all_id):
    cursor.execute(f'SELECT * FROM teachers WHERE school_id = "{all_id[:3]}" AND '
                   f'teacher_id = "{all_id[3:]}"')
    return cursor.fetchall()


def new_teacher_schoold_id(new_id):
    if len(new_id) != 3:
        return False
    login = dict_of_data.get('login')
    cursor.execute(f'SELECT name_of_subject FROM teachers WHERE school_id = "{login[:3]}"'  # взятие предмета учителя 
                   f'AND teacher_id = "{login[3:]}"')
    subject = cursor.fetchall()
    # print(subject)
    cursor.execute(f'SELECT * FROM teachers WHERE school_id = "{new_id}"'   # проверка на одинаковый предмет
                   f' AND name_of_subject = "{subject[0][0]}"')
    if cursor.fetchall():
        return False
    cursor.execute(f'SELECT * FROM teachers WHERE school_id = "{new_id}"'   # проверка на одинаковый учительский id
                   f' AND teacher_id = "{login[3:]}"')
    if cursor.fetchall():
        return False
    cursor.execute(f'UPDATE teachers SET school_id = "{new_id}" WHERE school_id = "{login[:3]}"'
                   f' AND teacher_id = "{login[3:]}"')  # если всё удовлетворяет, меняем
    conn.commit()
    dict_of_data['login'] = new_id + dict_of_data.get('login')[3:]
    return True


def new_teacher_id(new_id):
    if len(new_id) != 4:
        return False
    login = dict_of_data.get('login')
    cursor.execute(f'SELECT * FROM teachers WHERE school_id = "{login[:3]}" AND teacher_id = "{new_id}"')  # проверяем нет ли уже занятого такого же id
    if cursor.fetchall():
        return False
    cursor.execute(f'UPDATE teachers SET teacher_id = "{new_id}" WHERE teacher_id = "{login[3:]}"'
                   f' AND school_id = "{login[:3]}"')
    conn.commit()
    dict_of_data['login'] = dict_of_data.get('login')[:3] + new_id
    return True


def new_teacher_password(new_password):
    if len(new_password) > 32:
        return False
    login = dict_of_data.get('login')
    cursor.execute(f'UPDATE teachers SET password = "{new_password}" WHERE teacher_id = "{login[3:]}"'
                   f' AND school_id = "{login[:3]}"')
    conn.commit()
    return True


def new_teacher_subj(subj):
    if len(subj) > 15:
        return False
    login = dict_of_data.get('login')
    cursor.execute(f'SELECT name_of_subject FROM teachers '
                   f'WHERE name_of_subject = "{subj}" AND school_id = "{login[:3]}"')
    # проверяем нет ли такого же учителя уже, если есть, запрещаем создавать клона
    if cursor.fetchall():
        return False
    cursor.execute(f'UPDATE teachers SET name_of_subject = "{subj}" WHERE teacher_id = "{login[3:]}"'
                   f' AND school_id = "{login[:3]}"')
    conn.commit()
    return True


def delete_teacher():
    login = dict_of_data.get('login')
    cursor.execute(f'DELETE FROM teachers WHERE teacher_id = "{login[3:]}" AND school_id = "{login[:3]}"')
    conn.commit()


def grades():
    login = dict_of_data.get('login')
    cursor.execute(f'SELECT number_grade FROM grades WHERE school_id = "{login[:3]}"')
    return cursor.fetchall()


def change_homework(homework):  # функция на изменение домашки

    login, grade = dict_of_data.get('login'), dict_of_data.get('grade')
    cursor.execute(f'SELECT score FROM teachers WHERE school_id = "{login[:3]}" AND teacher_id = "{login[3:]}"')    # + прибавление балов за вход в меню выставления оценок
    tmp = cursor.fetchall()[0][0]
    if tmp is None:
        tmp = 3
    else:
        tmp = str(int(tmp) + 3)
    cursor.execute(f'UPDATE teachers SET score = "{tmp}" WHERE '
                   f'school_id = "{login[:3]}" AND teacher_id = "{login[3:]}"')
    conn.commit()

    cursor.execute(f'SELECT name_of_subject FROM teachers WHERE teacher_id = "{login[3:]}"'  # получаем из id предмет учителя
                   f' AND school_id = "{login[:3]}"')

    subject = cursor.fetchall()[0][0]
    cursor.execute(f'SELECT grade_id FROM grades WHERE school_id = "{login[:3]}"'   # получаем класс, который хотел редактировать учитель
                   f' AND number_grade = "{grade}"')

    grade_id = cursor.fetchall()
    if len(grade_id) == 0:
        return 'Такого класса не существует.\nПопробуйте заного(/room)'
    else:
        grade_id = grade_id[0][0]

    cursor.execute(f'SELECT * FROM homework WHERE school_id = "{login[:3]}" AND '   # запрос на проверку, есть ли вообще дз, если нет добавляем иначе, редачим
                   f'grade_id = "{grade_id}" AND subject = "{subject}"')

    if len(cursor.fetchall()) == 0:
        cursor.execute(f'INSERT INTO homework (school_id, grade_id, subject, homework) '     # добавление в таблицу нового дз на класс
                       f'VALUES ("{login[:3]}", "{grade_id}", "{subject}", "{homework}")')
    else:
        cursor.execute(f'UPDATE homework SET homework.homework = "{homework}" '  # обнговление дз в таблице
                       f'WHERE grade_id = "{grade_id}" AND school_id = "{login[:3]}" AND subject = "{subject}"')
    conn.commit()   # редактируем дз класса и комитим

    cursor.execute(f'SELECT homework FROM homework WHERE '      # выводим на экран. чтоб он мног проверить
                   f'grade_id = "{grade_id}" AND school_id = "{login[:3]}" AND subject = "{subject}"')
    result = cursor.fetchall()
    if result:
        return result[0][0]
    else:
        return 'Задание не удалось обновить.\nПопробуйте заного(/room)'


def check_grade():
    grade, school_id = dict_of_data.get('grade'), dict_of_data.get('login')[:3]
    cursor.execute(f'SELECT * FROM grades WHERE '
                   f'number_grade = "{grade}" AND school_id = "{school_id}"')
    if cursor.fetchall():
        return False
    return True


def create_school(id_new_school):   #  создание новой шк в базе данных
    if len(id_new_school) != 3:
        return False

    cursor.execute(f'SELECT * FROM schools WHERE school_id = "{id_new_school}"')    # проверяет если id уже занят
    if cursor.fetchall():
        return False

    new_school = 'Новосозданная школа'  # все поля с этой переменной будут позже редачится админом
    cursor.execute(f'INSERT INTO schools (name_school, slogan, school_id, news_of_school) '
                   f'VALUES ("{new_school}", "{new_school}", "{id_new_school}", "{new_school}")')
    conn.commit()   # заводим новую шк в бд
    dict_of_data['school_id'] = id_new_school
    return True


def set_title_of_school(title):
    if len(title) > 63:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute(f'SELECT * FROM schools WHERE name_school = "{title}"')  # проверяем нет ли у кого такого же названия
    if cursor.fetchall():
        return False
    cursor.execute(f'UPDATE schools SET name_school = "{title}" WHERE school_id = "{school_id}"')
    conn.commit()
    return True


def set_new_afisha(afisha):
    if len(afisha) > 511:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute(f'SELECT * FROM schools WHERE school_id = "{school_id}"')
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(f'UPDATE schools SET news_of_school = "{afisha}" WHERE school_id = "{school_id}"')
    conn.commit()
    return True


def check_school(school_id):
    cursor.execute(f'SELECT * FROM schools WHERE school_id = "{school_id}"')
    if cursor.fetchall():
        dict_of_data['school_id'] = school_id   # проверка введенной школы + занос в словарь
        return True
    else:
        return False


def create_grade(grade_id):
    if len(grade_id) != 3:
        return False
    cursor.execute(f'SELECT * FROM grades WHERE grade_id = "{grade_id}"')
    if len(cursor.fetchall()) != 0:
        return False
    school_id = dict_of_data.get('school_id')
    new_grade = 'Новый класс'
    # вводим новый класс в бд, поля new_grade позже буду заполненным инфой от админа
    cursor.execute(f'INSERT INTO grades (school_id, number_grade, grade_id, photo_teacher, name_of_teacher, invite_url, bulletin_board) '
                   f'VALUES ("{school_id}", "new", "{grade_id}", "{new_grade}", "{new_grade}", -1, "{new_grade}")')
    conn.commit()
    dict_of_data['grade_id'] = grade_id
    # так добавляем класс в расписания таблицу, чтоб в него давать раписания класса
    cursor.execute(f'INSERT INTO timetable (school_id, grade_id) VALUES'
                   f' ("{school_id}", "{grade_id}")')
    conn.commit()
    return True


def set_number(number):
    if len(number) > 7:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(f'SELECT * FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')     # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(f'SELECT * FROM grades WHERE school_id = "{school_id}" AND number_grade = "{number}"')   # проверяем нет ли уже такого номера в шк
    if cursor.fetchall():
        return False
    cursor.execute(f'UPDATE grades SET number_grade = "{number}" WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    conn.commit()
    return True


def set_photo(photo):
    if len(photo) > 127:
        return False
    photo = photo.replace('\\', '\\\\')
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        f'SELECT * FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(f'UPDATE grades SET photo_teacher = "{photo}" WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    conn.commit()
    return True


def set_grade_name_teacher(name_of_teacher):
    if len(name_of_teacher) > 63:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        f'SELECT * FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(
        f'UPDATE grades SET name_of_teacher = "{name_of_teacher}" WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    conn.commit()
    return True


def set_code(code):
    if len(code) > 63:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        f'SELECT * FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(
        f'UPDATE grades SET invite_url = {code} WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    conn.commit()
    return True


def set_desk(text):
    if len(text) > 1023:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        f'SELECT * FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')  # проверяем существукет ли такой класс
    if len(cursor.fetchall()) == 0:
        return False

    # махинация для добавления новости, и удалений старых
    cursor.execute(f'SELECT bulletin_board FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    news = cursor.fetchall()[0][0]
    news += text + '\n\n\n'
    while len(news) > 1023:
        news = news[news.find('\n\n\n'):]   # режем старые, если кончилось место

    cursor.execute(
        f'UPDATE grades SET bulletin_board = "{news}" WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')
    conn.commit()
    return True


def create_stud(name):
    if len(name) > 31:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(f'SELECT * FROM grades WHERE school_id = "{school_id}" AND grade_id = "{grade_id}"')  # проверяем классы
    if len(cursor.fetchall()) == 0:
        return False
    cursor.execute(f'INSERT INTO students (school_id, grade_id, name, stud_id) VALUES '  # заносим в таблицу
                   f'("{school_id}", "{grade_id}", "{name}", "-1")')
    conn.commit()
    dict_of_data['name'] = name
    return True


def set_stud_id(id):
    if len(id) > 3:
        return False
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute(
        f'SELECT * FROM students WHERE school_id = "{school_id}" AND grade_id = "{grade_id}" '
        f'AND stud_id = "{id}"')  # проверяем классы на клона, то есть чтоб не было такого же id
    if len(cursor.fetchall()) != 0:
        return False
    name = dict_of_data.get('name')
    cursor.execute(f'UPDATE students SET stud_id = "{id}" WHERE school_id = "{school_id}" AND grade_id = "{grade_id}" '
                   f'AND name = "{name}"')
    conn.commit()
    return True


def get_school(school_id):
    if len(school_id) > 3:
        return False
    cursor.execute(f'SELECT * FROM schools WHERE school_id = "{school_id}"')    # проверяем школу
    if len(cursor.fetchall()) == 0:
        return False
    dict_of_data['school_id'] = school_id
    return True


def create_teach(teacher_id):
    if len(teacher_id) > 4:
        return False
    new_teacher, school_id = '-1', dict_of_data.get('school_id')
    cursor.execute(f'SELECT * FROM teachers WHERE school_id = "{school_id}" AND teacher_id = "{teacher_id}"')   # если есть уже с такими id
    if len(cursor.fetchall()) != 0:
        return False
    # добавляем в бд, и потом редачим его
    cursor.execute(f'INSERT INTO teachers (school_id , teacher_id, password, name_of_subject, score) VALUES '
                   f'("{school_id}", "{teacher_id}", password = "-1", name_of_subject = "-1", score = "{str(0)}" )')
    conn.commit()
    dict_of_data['login'] = school_id + teacher_id
    return True


def set_name_of_school(name):
    if len(name) > 63:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute(f'UPDATE schools SET name_school = "{name}" WHERE school_id = "{school_id}"')
    conn.commit()
    return True


def set_news(news):
    if len(news) > 511:
        return False
    school_id = dict_of_data.get('school_id')
    cursor.execute(f'SELECT news_of_school FROM schools WHERE school_id = "{school_id}"')   # для добавления новой новости
    old_news = cursor.fetchall()[0][0]
    old_news += news + '\n\n\n'
    while len(old_news) > 511:   # если новостей уже много, режем пстарые новости
        old_news = old_news[old_news.find('\n\n\n') + 3:]
    cursor.execute(f'UPDATE schools SET news_of_school = "{old_news}" WHERE school_id = "{school_id}"')
    conn.commit()
    return True

if __name__ == '__main__':
    pass
