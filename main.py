import time

import telebot
from telebot import types
import datetime
import data


bot = telebot.TeleBot(data.TOKEN)


# def cleaner(chat_id, message_id):   # чистилка смс, если вдруг что-то пошло не по форме
#     for i in range(0, 21):
#         try:
#             bot.delete_message(chat_id, message_id - i)
#         except:
#             continue


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.from_user.id
    with open(data.get_res('first_pic'), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('first_ad'))  # получение текста рекламы
    bot.send_message(chat_id, data.get_list_of_schools())
    # получение всех школ участвующих в проекте
    msg = bot.send_message(chat_id, 'Введите индивидуальный код класса:')
    bot.register_next_step_handler(msg, second_step)


def board():
    # метод для кнопок на 2-ой форме,
    # каждая кнопка имеет свое id для метода
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    first_button = types.KeyboardButton(text='Расписание на завтра')
    second_button = types.KeyboardButton(text='Расписание по дням')
    markup.add(first_button, second_button)
    third_button = types.KeyboardButton(text='Доска объявлений')
    fourth_button = types.KeyboardButton(text='Классный чат')
    markup.add(third_button, fourth_button)
    markup.add(types.KeyboardButton(text='Афиша, новости'),
               types.KeyboardButton(text='Добашнее задание'))
    markup.add(types.KeyboardButton(text='Личный кабинет'))
    return markup


def second_step(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:            # ЕСЛИ НАДО БУДЕТ ОТМЕНИТЬ ВТОРУЮ РЕКЛАМУ
        bot.send_message(chat_id, 'Операция отменена.')
        return
    with open(data.get_res('second_pic'), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('second_ad'))  # получение второго текста рекламы

    grade = data.get_grade(message.text)  # получаем всю информацию о классе для формы
    if grade is None:   # если школа не найдена
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте'
                                        ' ещё раз(или введите *отмена*):')
        bot.register_next_step_handler(msg, second_step)
        return
    time.sleep(3)
    with open(grade[0][3], 'rb') as f:
        photo = f.read()  # получение фото классного руковод.
        bot.send_photo(chat_id, photo)
    bot.send_message(chat_id,
                     'ФИО Классного руководителя :\n' + grade[0][4] +
                     f'\n\nРасписание на {datetime.datetime.now().strftime("%d.%m.%Y")}:\n' +
                     data.trans(datetime.datetime.now().strftime("%A"), '\n'.join(grade[1])),
                     reply_markup=board())


def act_on_stud(stud_id):   # работа с учеником в меню админа
    markup = types.InlineKeyboardMarkup()
    stud_id = stud_id[:stud_id.find('sx')]
    markup.add(types.InlineKeyboardButton(text='Удалить', callback_data=stud_id + 'del'))
    markup.add(types.InlineKeyboardButton(text='Изменить код', callback_data=stud_id + 'edit'))
    return markup


@bot.callback_query_handler(func=lambda message: True)
def callback(obj):
    chat_id = obj.from_user.id
    # print(obj.data)
    # if obj.data == 'tt':  # код на завтрашний день
    #     timetable = data.get_timetable_on_tomorrow()
    #     bot.send_message(chat_id, timetable)

    # elif obj.data == 'chat':    # код на переход в беседу школьникв
    #     переход в другой чат, Серж
        # pass

    # elif obj.data == 'desk':    # код на доску
    #     bot.send_message(chat_id, data.get_desk())

    # elif obj.data == 'afisha':  # код на афишу
    #     bot.send_message(chat_id, data.get_afisha())

    # elif obj.data == 'room':    # код на комнату школьника
    #     msg = bot.send_message(chat_id, 'Введите персональный код ученика:')
    #     bot.register_next_step_handler(msg, person_room)

    # elif obj.data == 'allt':   # вывод всего расписания
    #     bot.send_message(chat_id, data.get_all_timetable())

    if obj.data == 'банер' or obj.data == 'текст':
        # смена админом банера или текста
        bot.send_message(chat_id, obj.data)
        msg = bot.send_message(chat_id, f'Какой {obj.data} вы хотите изменить?(1-ый или 2-ой)')
        bot.register_next_step_handler(msg, pre_change_banner_or_text)

    elif obj.data == 'смрасп':  # смена расписания выбранного класса
        msg = bot.send_message(chat_id, 'Введите код класса:')
        bot.register_next_step_handler(msg, pre_change_tt)

    elif obj.data == 'спуч':  # смена списка школьников
        msg = bot.send_message(chat_id, 'Введите код класса:')
        bot.register_next_step_handler(msg, pre_change_list_of_child)

    elif obj.data == 'пркод':  # выбор препод для изменения
        msg = bot.send_message(chat_id, 'Введите код преподователя,'
                                        ' который хотите изменить:')
        bot.register_next_step_handler(msg, change_id_teacher)

    elif obj.data == 'dz':  # выбор дз для изменения
        msg = bot.send_message(chat_id, 'Введите домашнее задание:')
        bot.register_next_step_handler(msg, change_homework)

    elif obj.data == 'ro':  # выбор дз для изменения
        teacher_edit(obj)

    # elif obj.data == 'homework':  # вывод домашнего задания   СДЕЛАТЬ!!!!
    #     bot.send_message(chat_id, data.print_hw())

    elif obj.data == 'сш':  # смена кода школы препода
        msg = bot.send_message(chat_id, 'Введите новый код школы (3 символа):')
        bot.register_next_step_handler(msg, change_school_teacher)

    elif obj.data == 'tid':  # смена айди препода
        msg = bot.send_message(chat_id, 'Введите новый код учителя (4 символа):')
        bot.register_next_step_handler(msg, change_teacher_id)

    elif obj.data == 'cp':  # смена пароля препода
        msg = bot.send_message(chat_id, 'Введите новый пароль'
                                        ' учителя (до 26 символов):')
        bot.register_next_step_handler(msg, change_teacher_password)

    elif obj.data == 'sub':  # смена предмета препода
        msg = bot.send_message(chat_id, 'Введите новый предмет для учителя:')
        bot.register_next_step_handler(msg, change_teacher_subj)

    elif obj.data == 'td':  # удаление препода
        data.delete_teacher()
        bot.send_message(chat_id, 'Операция выполнена успешно.')

    elif obj.data == 'cs':  # создание школы
        msg = bot.send_message(chat_id, 'Введите id новой школы(3 символа):')
        bot.register_next_step_handler(msg, create_school)

    elif obj.data == 'cg':  # создание класса
        msg = bot.send_message(chat_id, 'Введите id школы, в которой будет этот класс:')
        bot.register_next_step_handler(msg, create_grade)

    elif obj.data == 'cstud':   # создание студента
        msg = bot.send_message(chat_id, 'Введите id класса, в который хотите добавить ученика:')
        bot.register_next_step_handler(msg, pre_create_stud)

    elif obj.data == 'steach':  # создание учителя
        msg = bot.send_message(chat_id, 'Введите id школы, в которую добавить учителя:')
        bot.register_next_step_handler(msg, pre_create_teach)

    elif obj.data == 'школа':
        msg = bot.send_message(chat_id, 'Введите id школы которую хотите отредактировать:')
        bot.register_next_step_handler(msg, pre_edit_school)

    elif obj.data == 'назвшк':
        msg = bot.send_message(chat_id, 'Введите новое название школы:')
        bot.register_next_step_handler(msg, edit_name_of_school)

    elif obj.data == 'класс':
        msg = bot.send_message(chat_id, 'Введите id класса которого вы хотите редактировать:')
        bot.register_next_step_handler(msg, edit_grade)

    # elif obj.data == 'привки':
    #     msg = bot.send_message(chat_id, 'Введите новое приветствие школы:')
    #     bot.register_next_step_handler(msg, edit_slogan)

    elif obj.data == 'новыны':
        msg = bot.send_message(chat_id, 'Введите новую новость в школе:')
        bot.register_next_step_handler(msg, edit_news)

    elif obj.data == 'номкл':
        msg = bot.send_message(chat_id, 'Введите новый номер класса:')
        bot.register_next_step_handler(msg, new_number)

    elif obj.data == 'фотклрук':
        msg = bot.send_message(chat_id, 'Введите путь к новой фотографии классного рук.:')
        bot.register_next_step_handler(msg, photo_grade_teacher)

    elif obj.data == 'имклрук':
        msg = bot.send_message(chat_id, 'Введите новое имя классного рук.:')
        bot.register_next_step_handler(msg, set_grade_name_teacher2)

    elif obj.data == 'доскоб':
        msg = bot.send_message(chat_id, 'Введите новою информацию:')
        bot.register_next_step_handler(msg, set_desk2)

    elif obj.data.find('del') > -1:  # удаление школьника
        data.delete_stud(obj.data[:obj.data.find('del')])
        bot.send_message(chat_id, 'Операция прошла успешно.')

    elif obj.data.find('edit') > -1:   # изменение id школьника
        bot.send_message(chat_id, obj.data[:obj.data.find('edit')])
        msg = bot.send_message(chat_id, 'Введите новый код ученика (3 символа):')
        bot.register_next_step_handler(msg, accept_id)

    elif obj.data.find('sx') > -1:
        # работа с школьником, удаление, или изменение id
        bot.send_message(chat_id, 'Выберите действие :', reply_markup=act_on_stud(obj.data))

    else:   # код учителя, или же проставления оценки
        bot.send_message(chat_id, obj.data)
        msg = bot.send_message(chat_id, 'Введите оценку:')
        bot.register_next_step_handler(msg, accept)


def person_room(message):   # комната школьника
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    marks = data.get_marks(data.dict_of_data.get('school_id') + data.dict_of_data.get('grade_id') + message.text)
    # если код неверен выходим, если верен выводим оценки
    if marks is None:
        msg = bot.send_message(message.from_user.id, 'Неверный код, или у ученика нет оценок, '
                                                     'попробуйте ещё раз или пропишите "отмена" для выхода:')
        bot.register_next_step_handler(msg, person_room)
        return
    bot.send_message(chat_id, marks)   # выводим оценки


@bot.message_handler(commands=['room'])  # комната преподов
def room_of_teacher(message):
    msg = bot.send_message(message.from_user.id, 'Введите персональный код:')
    bot.register_next_step_handler(msg, pre_teacher_room)


def pre_teacher_room(message):
    if message.text.lower() == data.cancel_word:
        bot.send_message(message.from_user.id, 'Операция отменена.')
        return
    if data.check_teacher(message.text):
        # если препод есть идем дальше, иначе выкидываем
        msg = bot.send_message(message.from_user.id, 'Неверный код, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, pre_teacher_room)
        return
    msg = bot.send_message(message.from_user.id, 'Введите пароль:')
    bot.register_next_step_handler(msg, teacher_room)


def grades(ls_of_grades):   # генератор списка классов
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i in ls_of_grades:
        markup.add(types.KeyboardButton(text=i[0]))
    return markup


def teacher_room(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    teacher = data.check_pass(message.text)
    if teacher is None:  # проверка на пароль
        # cleaner(chat_id, message.message_id)
        bot.send_message(message.from_user.id, 'Неверный пароль, если хотите '
                                               'продолжить переавторизируйтесь (/room)')
        return
    ls_of_grades = data.grades()   # получаем из id учителя все классы(т.к. есть school_id)
    msg = bot.send_message(message.from_user.id, 'Введите класс:',
                           reply_markup=grades(ls_of_grades))
    bot.register_next_step_handler(msg, change_hw_or_marks)


def action():   # кнопки после ввода класса
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Домашнее задание', callback_data='dz'))
    markup.add(types.InlineKeyboardButton(text='Расставление оценок', callback_data='ro'))
    return markup


def change_hw_or_marks(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    data.dict_of_data['grade'] = message.text
    if data.check_grade():
        # cleaner(chat_id, message.message_id)
        bot.send_message(chat_id, 'Введенный класс не сущесвует, чтобы '
                                  'продолжить переавторизируйтесь (/room)')
        return
    bot.send_message(chat_id, 'Выберите действие: ',
                     reply_markup=action())


def change_homework(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        # cleaner(chat_id, message.message_id)
        return
    # получаем все данные, а именно логин, класс, дз
    new_task = data.change_homework(message.text)
    # cleaner(chat_id, message.message_id)
    if new_task.find('/room') != -1:
        bot.send_message(chat_id, new_task)
    else:
        bot.send_message(chat_id, 'Задание было успешно обновленно;\nНовое задание: \n' + new_task
                         + '\nДля продолжения работы, переавторизуйтесь(/room).')


def teacher_edit(message):
    chat_id = message.from_user.id
    if message.data.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    magazine = data.magazine()
    if len(magazine) == 0:
        # cleaner(chat_id, message.message.message_id)
        bot.send_message(chat_id, 'Выбранный класс не существует,'
                                  ' для продолжения переавторизируйтесь (/room)')
        return
    # получаем всех учеников и выводим их списком
    markup = types.InlineKeyboardMarkup()
    for i in magazine:
        markup.add(types.InlineKeyboardButton(text=i[i.find(':') + 1:], callback_data=i[:i.find(':')]))
    bot.send_message(chat_id, 'Список учеников :', reply_markup=markup)


def accept(message):    # установка оценки,
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 2)
    stud_id = temp_message.text
    # получаем код ученика и редачим его оценку
    bot.delete_message(chat_id, message.message_id - 2)
    bot.delete_message(chat_id, temp_message.message_id)
    data.set_mark(message.text, stud_id)
    # устанавливаем оценку, чистим все лишнее
    # cleaner(chat_id, message.message_id)
    bot.send_message(chat_id, 'Оценка успешно установленна.\n'
                              'Для продолжения работы, переавторизуйтесь(/room).')


@bot.message_handler(commands=['admin'])    # панель админа
def admin(message):
    msg = bot.send_message(message.from_user.id, 'Введите пароль:')
    bot.register_next_step_handler(msg, admin_room)


def admin_butt():   # клавиатурка админа
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Банер', callback_data='банер'),
               types.InlineKeyboardButton(text='Текст', callback_data='текст'))
    markup.add(types.InlineKeyboardButton(text='Школа', callback_data='школа'),
               types.InlineKeyboardButton(text='Класс', callback_data='класс'))
    markup.add(types.InlineKeyboardButton(text='Расписание', callback_data='смрасп'))
    markup.add(types.InlineKeyboardButton(text='Учеников', callback_data='спуч'),
               types.InlineKeyboardButton(text='Преподователей', callback_data='пркод'))
    return markup


def admin_butt2():   # клавиатурка админа на создание
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Школу', callback_data='cs'),
               types.InlineKeyboardButton(text='Класс', callback_data='cg'))
    markup.add(types.InlineKeyboardButton(text='Ученика', callback_data='cstud'),
               types.InlineKeyboardButton(text='Учителя', callback_data='steach'))
    return markup


def admin_room(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if message.text != data.dict_of_admins.get(chat_id):
        bot.send_message(message.from_user.id, 'Неверный пароль.\nДля продолжения работы переавторизируйтесь (/admin)')
        return
    # если все успешно, то есть пароль ок,
    # то ты в комнате админа
    bot.send_message(chat_id, 'Редактировать:', reply_markup=admin_butt())
    bot.send_message(chat_id, 'Создать:', reply_markup=admin_butt2())


def pre_change_banner_or_text(message):
    # получаем информацию, а именно что надо изменить
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 2)
    change_type = temp_message.text
    bot.delete_message(chat_id, temp_message.message_id)
    if data.check_ad(change_type, message.text):
        bot.send_message(chat_id, f'Нужного {change_type}а не найдено.')
        return
    # проверка есть ли такая реклама
    msg = bot.send_message(chat_id,
                           'Введите новую информацию :\n(банер - путь'
                           ' к картинке,\nтекст - сам текст):')
    bot.register_next_step_handler(msg, change_banner_or_text)


def change_banner_or_text(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 5)
    change_type = temp_message.text
    bot.delete_message(chat_id, temp_message.message_id)
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 3)
    number_ad = temp_message.text
    bot.delete_message(chat_id, temp_message.message_id)
    # после получение всей инфы, меняем банер, или рекламный текст
    data.change_ad(change_type, number_ad, message.text.replace('\\', '\\\\'))
    bot.send_message(chat_id, 'Операция успешно завершена.')


def days_tt():  # клавиатурка для расписания
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Понедельник'), types.KeyboardButton(text='Вторник'))
    markup.add(types.KeyboardButton(text='Среда'), types.KeyboardButton(text='Четверг'))
    markup.add(types.KeyboardButton(text='Пятница'), types.KeyboardButton(text='Суббота'))
    return markup


def pre_change_tt(message):  # функция для ввода дня изменяемого раписанием
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.get_grade(message.text) is None:
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте заного ввести код:')
        bot.register_next_step_handler(msg, pre_change_tt)
        return
    msg = bot.send_message(chat_id, 'Кликните на день, который хотите изменить:',
                           reply_markup=days_tt())
    # выбор через клавиатурку дня для смены расписания
    bot.register_next_step_handler(msg, pre_change_tt2)


def pre_change_tt2(message):  # функция для ввода расписания
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    ls_of_days = ['Понедельник', 'Вторник', 'Среда',
                  'Четверг', 'Пятница', 'Суббота']
    if message.text not in ls_of_days:
        bot.send_message(chat_id, 'Вы не выбрали день.\n'
                                  'Для продолжения работы '
                                  'переавторизируйтесь(/admin)')
        return
    msg = bot.send_message(chat_id, 'Введите новое '
                                    'расписание (символ-разделитель - ; ):')
    # ввод нового расписания, символ разделитель это для
    # смещение коретки на некст строку
    bot.register_next_step_handler(msg, change_tt)


def change_tt(message):  # функция на смену расписания
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 2)
    day = temp_message.text
    bot.delete_message(chat_id, temp_message.message_id)
    data.set_tt(message.text, day)
    # установка расписания
    bot.send_message(chat_id, 'Операция успешно завершена.')


def studs(ls_of_stud):  # генерация кнопок студентов
    markup = types.InlineKeyboardMarkup()
    for i in ls_of_stud:
        markup.add(types.InlineKeyboardButton(text=i[:i.find(':')], callback_data=i[i.find(':') + 1:] + 'sx'))
    return markup


def pre_change_list_of_child(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    ls_of_stud = data.check_stud(message.text)
    if ls_of_stud is None:
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, pre_change_list_of_child)
        return
    bot.send_message(chat_id, 'Список учеников, кликните для редактирования :',
                     reply_markup=studs(ls_of_stud))


def accept_id(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 2)
    old_stud_id = temp_message.text
    bot.delete_message(chat_id, temp_message.message_id)
    # cleaner(chat_id, message.message_id)
    if data.change_id(message.text, old_stud_id):
        bot.send_message(chat_id, f'Операция успешно завершена.\n'
                                  f'ID ученика : {message.text}')
    else:
        bot.send_message(chat_id, 'Выбранный ID не подходит, попробуйте другой.')


def buttons_of_teacher(teacher_id):  # клавиатурка для игры с учителем
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Сменить школу', callback_data='сш'),
               types.InlineKeyboardButton(text='Сменить id', callback_data='tid'))
    markup.add(types.InlineKeyboardButton(text='Сменить пароль', callback_data='cp'),
               types.InlineKeyboardButton(text='Сменить предмет', callback_data='sub'))
    markup.add(types.InlineKeyboardButton(text='Удалить', callback_data='td'))
    return markup


def change_id_teacher(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    try:
        info = data.check_teacher_id(message.text)[0]
    except:
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, change_id_teacher)
    else:
        data.dict_of_data['login'] = message.text   # вывод инфы о учителе
        info = list(info)
        info[0] = 'Код школы: ' + info[0]
        info[1] = 'Код учителя: ' + info[1]
        info[2] = 'Пароль учителя: ' + info[2]
        info[3] = 'Предмет учителя: ' + info[3]
        info[4] = 'Баллы учителя: ' + info[4]
        bot.send_message(chat_id, 'Данные учителя :\n' + '\n'.join(info),
                         reply_markup=buttons_of_teacher(message.text))


# далее все методы изменения учителя


def change_school_teacher(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.new_teacher_schoold_id(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена.')
    else:
        bot.send_message(chat_id, 'Выбранный ID не подходит, если хотите продолжить'
                                  ' переавторизуйтесь (/admin)')


def change_teacher_id(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.new_teacher_id(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена.')
    else:
        bot.send_message(chat_id, 'Выбранный ID не подходит, если хотите продолжить '
                                  'переавторизуйтесь (/admin)')


def change_teacher_password(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.new_teacher_password(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена.')
    else:
        msg = bot.send_message(chat_id, 'Пароль не может быть таким, введите другой:')
        bot.register_next_step_handler(msg, change_teacher_password)


def change_teacher_subj(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.new_teacher_subj(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена.')
    else:
        msg = bot.send_message(chat_id, 'Этот предмет препадает другой учитель, введите новый:')
        bot.register_next_step_handler(msg, change_teacher_subj)


def create_school(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.create_school(message.text):
        msg = bot.send_message(chat_id, 'Школа успешно созданна, введите название новой школы:')
        bot.register_next_step_handler(msg, new_title_of_school)
    else:
        msg = bot.send_message(chat_id, 'Введенный id не подходит, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, create_school)


def new_title_of_school(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_title_of_school(message.text):
        msg = bot.send_message(chat_id, 'Название школы успешно установленно, введите афишу школы:')
        bot.register_next_step_handler(msg, new_afisha_of_school)
    else:
        msg = bot.send_message(chat_id, 'Введенное название существует, попробуйте ввести другое:')
        bot.register_next_step_handler(msg, new_title_of_school)


# def new_slogan_of_school(message):
#     chat_id = message.from_user.id
#     if message.text.lower() == data.cancel_word:
#         bot.send_message(chat_id, 'Операция отменена.')
#         return
#     if data.set_new_slogan(message.text):
#         msg = bot.send_message(chat_id, 'Слоган школы успешно установленн, введите афишу школы:')
#         bot.register_next_step_handler(msg, new_afisha_of_school)
#     else:
#         msg = bot.send_message(chat_id, 'Введенный текст не подходит, введите новый:')
#         bot.register_next_step_handler(msg, new_slogan_of_school)


def new_afisha_of_school(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_new_afisha(message.text):
        bot.send_message(chat_id, 'Школа успешно созданна.')
    else:
        msg = bot.send_message(chat_id, 'Введенный текст не подходит, введите новый:')
        bot.register_next_step_handler(msg, new_afisha_of_school)


def create_grade(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.check_school(message.text):  # проверка, существует ли введенная школа
        msg = bot.send_message(chat_id, 'Введите id класса:')
        bot.register_next_step_handler(msg, new_grade)
    else:
        msg = bot.send_message(chat_id, 'Школа с введенным id не найдена, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, create_grade)


def new_grade(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.create_grade(message.text):
        msg = bot.send_message(chat_id, 'Класс создан, введите номер класса:')
        bot.register_next_step_handler(msg, set_number)
    else:
        msg = bot.send_message(chat_id, 'Введенный id не подходит, введите новый:')
        bot.register_next_step_handler(msg, new_grade)


def set_number(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_number(message.text):
        msg = bot.send_message(chat_id, 'Номер установлен, введите фотографию(путь к файлу) классного руководителя:')
        bot.register_next_step_handler(msg, set_photo)
    else:
        msg = bot.send_message(chat_id, 'Введенный номер не подходит, введите новый:')
        bot.register_next_step_handler(msg, set_number)


def set_photo(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_photo(message.text):
        msg = bot.send_message(chat_id, 'Фотография установленна, введите имя классного руководителя:')
        bot.register_next_step_handler(msg, set_grade_name_teacher)
    else:
        msg = bot.send_message(chat_id, 'Введнный путь не подходит, введите новый:')
        bot.register_next_step_handler(msg, set_photo)


def set_grade_name_teacher(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_grade_name_teacher(message.text):
        msg = bot.send_message(chat_id, 'Имя классного рук. установленно, введите код беседы(если нет то -1):')
        bot.register_next_step_handler(msg, set_code)
    else:
        msg = bot.send_message(chat_id, 'Введеное имя не подходит, введите новое:')
        bot.register_next_step_handler(msg, set_grade_name_teacher)


def set_code(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_code(message.text):
        msg = bot.send_message(chat_id, 'Invite Url установлен, введите текст доски объявлений:')
        bot.register_next_step_handler(msg, set_desk)
    else:
        msg = bot.send_message(chat_id, 'Введеный url не подходите, введите новый:')
        bot.register_next_step_handler(msg, set_code)


def set_desk(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_desk(message.text):
        bot.send_message(chat_id, 'Класс успешно создан')
    else:
        msg = bot.send_message(chat_id, 'Введенная информация не подходит, введите новую:')
        bot.register_next_step_handler(msg, set_desk)


def pre_create_stud(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.get_grade(message.text) is not None:
        msg = bot.send_message(chat_id, 'Введенная введите имя нового ученика:')
        bot.register_next_step_handler(msg, create_stud)
    else:
        msg = bot.send_message(chat_id, 'Введенного класса не сущесвует, попробуйте заного:')
        bot.register_next_step_handler(msg, pre_create_stud)


def create_stud(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.create_stud(message.text):
        msg = bot.send_message(chat_id, 'Имя установлено, введите id нового ученика:')
        bot.register_next_step_handler(msg, set_stud_id)
    else:
        msg = bot.send_message(chat_id, 'Введенное имя не подходит, введите новое:')
        bot.register_next_step_handler(msg, create_stud)


def set_stud_id(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_stud_id(message.text):
        bot.send_message(chat_id, 'Новый ученик добавлен.')
    else:
        msg = bot.send_message(chat_id, 'Введенный id не подходит, введите новый:')
        bot.register_next_step_handler(msg, set_stud_id)


def pre_create_teach(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.get_school(message.text):
        msg = bot.send_message(chat_id, 'Введите преподовательский id:')
        bot.register_next_step_handler(msg, create_teach)
    else:
        msg = bot.send_message(chat_id, 'Школы с введенным id не существует, попробуйте ввести ещё раз:')
        bot.register_next_step_handler(msg, pre_create_teach)


def create_teach(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.create_teach(message.text):
        msg = bot.send_message(chat_id, 'Введите пароль учителя:')
        bot.register_next_step_handler(msg, create_teacher_password)
    else:
        msg = bot.send_message(chat_id, 'Введенный id не подходит, попробуйте снова:')
        bot.register_next_step_handler(msg, create_teach)


def create_teacher_password(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.new_teacher_password(message.text):
        msg = bot.send_message(chat_id, 'Введите предмет учителя:')
        bot.register_next_step_handler(msg, create_teacher_subj)
    else:
        msg = bot.send_message(chat_id, 'Пароль не может быть таким, введите другой:')
        bot.register_next_step_handler(msg, create_teacher_password)


def create_teacher_subj(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.new_teacher_subj(message.text):
        bot.send_message(chat_id, 'Учитель успешно добавлен.')
    else:
        msg = bot.send_message(chat_id, 'Этот предмет не может быть привязан к данному учителю, введите другой:')
        bot.register_next_step_handler(msg, create_teacher_subj)


def edit_school():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Название школы', callback_data='назвшк'))
    markup.add(types.InlineKeyboardButton(text='Новости школы', callback_data='новыны'))
    return markup


def pre_edit_school(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.get_school(message.text):
        bot.send_message(chat_id, 'Редактировать:', reply_markup=edit_school())
    else:
        msg = bot.send_message(chat_id, 'Школы с введенным id не найдено, введите ещё раз id:')
        bot.register_next_step_handler(msg, pre_edit_school)


def edit_name_of_school(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_name_of_school(message.text):
        bot.send_message(chat_id, 'Название школы успешно изменено.')
    else:
        msg = bot.send_message(chat_id, 'Введите другое название школы:')
        bot.register_next_step_handler(msg, edit_name_of_school)
#
#
# def edit_slogan(message):
#     chat_id = message.from_user.id
#     if message.text.lower() == data.cancel_word:
#         bot.send_message(chat_id, 'Операция отменена.')
#         return
#     if data.set_slogan(message.text):
#         bot.send_message(chat_id, 'Приветствие школы успешно изменено.')
#     else:
#         msg = bot.send_message(chat_id, 'Введите другое привествие школы:')
#         bot.register_next_step_handler(msg, edit_slogan)


def edit_news(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_news(message.text):
        bot.send_message(chat_id, 'Новости школы обновлены.')
    else:
        msg = bot.send_message(chat_id, 'Новости слишком велика, введите заного:')
        bot.register_next_step_handler(msg, edit_news)


def grade_butt():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Номер класса', callback_data='номкл'))
    markup.add(types.InlineKeyboardButton(text='Фото классного руководителя', callback_data='фотклрук'))
    markup.add(types.InlineKeyboardButton(text='Имя классного руководителя', callback_data='имклрук'))
    markup.add(types.InlineKeyboardButton(text='Доска объявлений', callback_data='доскоб'))
    return markup


def edit_grade(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.get_grade(message.text) is not None:
        bot.send_message(chat_id, 'Редактировать:', reply_markup=grade_butt())
    else:
        msg = bot.send_message(chat_id, 'Класса с введенным id не существует, введите id заного:')
        bot.register_next_step_handler(msg, edit_grade)


def new_number(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_number(message.text):
        bot.send_message(chat_id, 'Номер класса установлен.')
    else:
        msg = bot.send_message(chat_id, 'Новый номер класса недопустим, введите другой:')
        bot.register_next_step_handler(msg, new_number)


def photo_grade_teacher(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_photo(message.text):
        bot.send_message(chat_id, 'Фото класного руководителя установлено.')
    else:
        msg = bot.send_message(chat_id, 'Путь неверный, введите новый путь:')
        bot.register_next_step_handler(msg, photo_grade_teacher)


def set_grade_name_teacher2(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_grade_name_teacher(message.text):
        msg = bot.send_message(chat_id, 'Имя классного рук. установленно.')
    else:
        msg = bot.send_message(chat_id, 'Введеное имя не подходит, введите новое:')
        bot.register_next_step_handler(msg, set_grade_name_teacher2)


def set_desk2(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_desk(message.text):
        bot.send_message(chat_id, 'Доска обновлена')
    else:
        msg = bot.send_message(chat_id, 'Введенная информация не подходит, введите новую:')
        bot.register_next_step_handler(msg, set_desk)


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    text = message.text
    if text == 'Расписание на завтра':
        timetable = data.get_timetable_on_tomorrow()
        bot.send_message(chat_id, timetable)
    elif text == 'Расписание по дням':
        bot.send_message(chat_id, data.get_all_timetable())
    elif text == 'Доска объявлений':
        bot.send_message(chat_id, data.get_desk())
    elif text == 'Классный чат':
        return
    elif text == 'Афиша, новости':
        bot.send_message(chat_id, data.get_afisha())
    elif text == 'Добашнее задание':
        bot.send_message(chat_id, data.print_hw())
    elif text == 'Личный кабинет':
        msg = bot.send_message(chat_id, 'Введите персональный код ученика:')
        bot.register_next_step_handler(msg, person_room)


if __name__ == '__main__':
    bot.infinity_polling(True)
