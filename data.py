import mysql.connector
import datetime

TOKEN = '914271777:AAGrCkpUMSUKOeg0VOh06eyz-XF-gXxQa34'

conn = mysql.connector.connect(user='root', password='0000001', host='127.0.0.1', database='tgbot')
cursor = conn.cursor(buffered=True)

dict_of_data = {'login': '0', 'password': '0', 'grade': '0',
                'school_id': '0', 'grade_id': '0', 'name': '0',
                'stud_id': [], 'last_stud_id': '0', 'ad': '0'}   # словарь с аудентификаторными данными
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
    result_str = ''
    for i in cursor.fetchall():
        result_str += i[0] + '\n'
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
        return answer


def get_all_timetable():
    school_id, grade_id = dict_of_data.get('school_id'), dict_of_data.get('grade_id')
    cursor.execute('SELECT * FROM timetable WHERE school_id = "{}" '
                   'AND grade_id = "{}"'.format(school_id, grade_id))
    answer = list(cursor.fetchall()[0][2:])
    try:
        answer[0] = 'Понедельник\n' + answer[0]
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
    if len(id) > 9:
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
    grade_id = dict_of_data['grade_id'] = cursor.fetchall()[0][0]
    cursor.execute('SELECT name, stud_id FROM students '
                   'WHERE grade_id = "{}" AND school_id = "{}"'.format(grade_id, login[:3]))
    # получение списка всех студентов
    ls_of_result = []
    for i in cursor.fetchall():
        ls_of_result.append(i[1] + ':' + i[0])
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
    cursor.execute('SELECT name_of_subject FROM teachers '     # получаем предмет учителя
                   'WHERE school_id = "{}" AND teacher_id = "{}"'.format(login[:3], login[3:]))
    cursor.execute('INSERT INTO marks (school_id, grade_id, stud_id , name_of_subject , mark) '
                   'VALUES ("{}", "{}", "{}", "{}", "{}")'.format(login[:3], grade_id, stud_id, cursor.fetchall()[0][0], mark))
    # из полученных данных в инфо, выбираем предмет, айди студа и ставим в него оценку
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
    dict_of_days_rus = {'Понедельник': 'Mon', 'Вторник': 'Tue', 'Среда': 'Wed',  # для внесения в бд нового расписания(по колонкам дни на англ)
                        'Четверг': 'Thu', 'Пятница': 'Fri', 'Суббота': 'Sat'}
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
    if len(stud_id) != 3:
        return False
    school_id = dict_of_data.get('school_id')
    grade_id = dict_of_data.get('grade_id')
    old_stud_id = dict_of_data.get('last_stud_id')[:3]  # режим от edit, так как пометка на инлайн
    cursor.execute('SELECT * FROM students WHERE stud_id = "{}" AND school_id = "{}" '
                   'AND grade_id = "{}"'.format(stud_id, school_id, grade_id))
    if cursor.fetchall():   # если id занят или ещё что-то не так
        return False
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
    if len(subj) > 15:
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
    if len(code) > 45 or code.find('https://t.me/joinchat/') == -1:
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
    if len(id) > 3:
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


if __name__ == '__main__':
    pass
