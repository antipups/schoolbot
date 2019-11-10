import random
import time
import requests
import telebot
from telebot import types
import datetime
import data
import os


bot = telebot.TeleBot(data.TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.from_user.id
    number_of_ad = str(random.randint(1, 5))
    with open(data.get_res('картинка' + number_of_ad), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('реклама' + number_of_ad))  # получение текста рекламы
    bot.send_message(chat_id, '🏫 Школы учавствующие в проекте 🏫\n' + data.get_list_of_schools())
    # получение всех школ участвующих в проекте
    msg = bot.send_message(chat_id, 'Введите индивидуальный код класса (6 символов):', reply_markup=cancel_key())
    bot.register_next_step_handler(msg, second_step)


def board():
    # метод для кнопок на 2-ой форме,
    # каждая кнопка имеет свое id для метода
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    first_button = types.KeyboardButton(text='📆Расписание на завтра')
    second_button = types.KeyboardButton(text='🗓Расписание по дням')
    fourth_button = types.KeyboardButton(text='💬Чат')
    markup.add(first_button, second_button)
    # third_button = types.KeyboardButton(text='📋Доска объявлений')
    # markup.add(types.KeyboardButton(text='📰Афиша, новости'),
    #            types.KeyboardButton(text='📖Домашнее задание'))
    markup.add(fourth_button, types.KeyboardButton(text='Оценки'))
    return markup


def cancel_key():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Отмена'))
    return markup


def second_step(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=cancel_key())
        return
    number_of_ad = str(random.randint(1, 5))
    with open(data.get_res('картинка' + number_of_ad), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('реклама' + number_of_ad))  # получение второго текста рекламы

    grade = data.get_grade(message.text)  # получаем всю информацию о классе для формы
    if grade is None:   # если школа не найдена
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте'
                                        ' ещё раз (или нажмите кнопку *Отмена*):', reply_markup=cancel_key())
        bot.register_next_step_handler(msg, second_step)
        return
    time.sleep(3)
    with open(grade[0][3], 'rb') as f:
        photo = f.read()  # получение фото классного руковод.
        bot.send_photo(chat_id, photo)
    # name_of_day = data.trans(datetime.datetime.now().strftime("%A"), '\n'.join(grade[1]))
    # name_of_day, timetable = name_of_day[:name_of_day.find('\n')], name_of_day[name_of_day.find('\n'):]
    bot.send_message(chat_id, grade[0][4] +
                     # '\n\nРасписание на {} {}:'.format(name_of_day, datetime.datetime.now().strftime("%d.%m.%Y")) + timetable,
                     "\nСм. кнопки ниже 👇",
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

    if obj.data == 'dz':  # выбор дз для изменения
        bot.delete_message(chat_id, obj.message.message_id)
        msg = bot.send_message(chat_id, 'Введите домашнее задание:')
        bot.register_next_step_handler(msg, change_homework)

    elif obj.data == 'ro':  # выбор дз для изменения
        bot.delete_message(chat_id, obj.message.message_id)
        teacher_edit(obj)

    elif obj.data == 'subjects':
        edit_subject_in_class(obj)

    elif obj.data == 'dz_class':  # выбор дз для изменения
        bot.delete_message(chat_id, obj.message.message_id)
        msg = bot.send_message(chat_id, 'Введите домашнее задание:')
        bot.register_next_step_handler(msg, change_homework_class)

    elif obj.data == 'ro_class':  # выбор дз для изменения
        bot.delete_message(chat_id, obj.message.message_id)
        teacher_edit_class(obj)

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

    elif obj.data == 'ttable':
        pre_change_tt(obj)

    elif obj.data == 'ссылпригл':
        pre_edit_url_of_invite(obj)

    elif obj.data == 'назвшк':
        msg = bot.send_message(chat_id, 'Введите новое название школы:')
        bot.register_next_step_handler(msg, edit_name_of_school)

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

    elif obj.data == 'удлшк':
        data.delete_school()
        bot.send_message(chat_id, 'Операция прошла успешно.')

    elif obj.data == 'удкл':
        data.delete_grade()
        bot.send_message(chat_id, 'Операция прошла успешно.')

    elif obj.data.find('del') > -1:  # удаление школьника
        data.delete_stud(obj.data[:obj.data.find('del')])
        bot.send_message(chat_id, 'Операция прошла успешно.')

    elif obj.data.find('edit') > -1:   # изменение id школьника
        data.dict_of_data['last_stud_id'] = obj.data
        msg = bot.send_message(chat_id, 'Введите новый код ученика (3 символа):')
        bot.register_next_step_handler(msg, accept_id)

    elif obj.data.find('sx') > -1:
        # работа с школьником, удаление, или изменение id
        bot.send_message(chat_id, 'Выберите действие :', reply_markup=act_on_stud(obj.data))

    else:   # код учителя, или же проставления оценки
        bot.delete_message(chat_id, obj.message.message_id - 1)
        bot.delete_message(chat_id, obj.message.message_id)
        data.dict_of_data['last_stud_id'] = obj.data
        msg = bot.send_message(chat_id, 'Введите оценку:')
        bot.register_next_step_handler(msg, accept)


def person_room(message):   # комната школьника
    chat_id = message.from_user.id
    if message.text.lower().find('отмена') > -1:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.dict_of_data.get('student') == '0':
        marks = data.get_marks(data.dict_of_data.get('school_id') + data.dict_of_data.get('grade_id') + message.text)
        data.dict_of_data['student'] = message.text
    else:
        marks = data.get_marks(data.dict_of_data.get('school_id') + data.dict_of_data.get('grade_id') + data.dict_of_data.get('student'))
    # если код неверен выходим, если верен выводим оценки
    if marks == 'Оценок нет.' or marks == 'Код ученика введен не по форме.':
        bot.send_message(message.from_user.id, marks)
        if marks == 'Код ученика введен не по форме.':
            data.dict_of_data['student'] = '0'
        return
    bot.send_message(chat_id, marks, parse_mode='Markdown')   # выводим оценки
    number_of_ad = str(random.randint(1, 5))
    with open(data.get_res('картинка' + number_of_ad), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('реклама' + number_of_ad ))  # получение текста рекламы


@bot.message_handler(commands=['room'])  # комната преподов
def room_of_teacher(message):
    msg = bot.send_message(message.from_user.id, 'Введите персональный код до 7 цифр:', reply_markup=cancel_key())
    bot.register_next_step_handler(msg, pre_teacher_room)


def pre_teacher_room(message):
    if message.text.lower() == data.cancel_word:
        bot.send_message(message.from_user.id, 'Операция отменена.')
        return
    if data.check_teacher(message.text):
        # если препод есть идем дальше, иначе выкидываем
        msg = bot.send_message(message.from_user.id, 'Неверный код, попробуйте ещё раз или нажмите кнопку *Отмена*:',
                               reply_markup=cancel_key())
        bot.register_next_step_handler(msg, pre_teacher_room)
        return
    msg = bot.send_message(message.from_user.id, 'Введите пароль:', reply_markup=cancel_key())
    bot.register_next_step_handler(msg, teacher_room)


def grades(ls_of_grades):   # генератор списка классов
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    for i in ls_of_grades:
        markup.add(types.KeyboardButton(text=i))
    markup.add(types.KeyboardButton(text='Отмена'))
    return markup


def keyboard_of_subjects_for_teacher():
    result = data.get_all_subjects_for_teacher()
    if result:  # если предметы есть, заходим в меню и выводим все предметы, иначе не выводим меню, а говорим что тут пусто
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for i in result:
            markup.add(types.KeyboardButton(text=i[0]))
        markup.add(types.KeyboardButton(text='Вернуться в меню'))
        return markup
    return False


def keyboard_for_only_grade():
    result = data.return_subjects_of_grade()
    if result:  # если предметы есть, заходим в меню и выводим все предметы, иначе не выводим меню, а говорим что тут пусто
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for i in result:
            markup.add(types.KeyboardButton(text=i[0]))
        markup.add(types.KeyboardButton(text=data.back_word))
        return markup
    return False


def teacher_room(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    teacher = data.check_pass(message.text)
    if teacher is None:  # проверка на пароль
        msg = bot.send_message(message.from_user.id, 'Неверный пароль, попробуйте ввести ещё раз,'
                                                     ' или нажмите кнопку *Отмена*:', reply_markup=cancel_key())
        bot.register_next_step_handler(msg, teacher_room)
        return

    classroom_teacher = data.check_classroom_teacher()      # ПРОВЕРКА НА КЛАССНОГО РУКОВОДИТЕЛЯ
    if classroom_teacher:
        if keyboard_of_subjects_for_teacher() is False:
            bot.send_message(chat_id, 'Предметов / класса нет.')
            return
        msg = bot.send_message(chat_id, 'Выберите устанавливаемый предмет:',
                               reply_markup=keyboard_of_subjects_for_teacher())
        bot.register_next_step_handler(msg, for_class_room)
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


def action_for_class():   # кнопки для классного руководителя
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Домашнее задание', callback_data='dz_class'))
    markup.add(types.InlineKeyboardButton(text='Расставление оценок', callback_data='ro_class'))
    return markup


def for_class_room(message):
    chat_id = message.from_user.id
    if message.text.lower() == 'вернуться в меню':
        bot.send_message(chat_id, 'Операция отменена.')
        return
    for i in data.get_all_subjects():
        if i[1] == message.text:
            data.dict_of_data['subject'] = message.text
            bot.send_message(chat_id, 'Выберите действие: ',
                             reply_markup=action_for_class())
            return
    else:
        bot.register_next_step_handler(bot.send_message(chat_id,
                                                        'Предмета не найдено в списке предметов, '
                                                        'попробуйте ещё раз:'), for_class_room)


def change_homework_class(message):     # меняем дз будучи классным руководителем
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    new_task = data.change_homework_for_class(message.text)
    bot.send_message(chat_id, new_task)
    bot.send_message(chat_id, 'Выберите действие:', reply_markup=action_for_class())


def teacher_edit_class(message):
    chat_id = message.from_user.id
    try:    # если пользователь ошибся и перехотел вводить заного
        message.data.lower()
    except AttributeError:
        if message.text.lower() == data.cancel_word:
            bot.send_message(chat_id, 'Операция отменена.')
            return
        msg = bot.send_message(chat_id, 'В веденном классе нет учеников, попробуйте выбрать другой класс,'
                                        'или нажмите *Отмена* для выхода:')
        bot.register_next_step_handler(msg, teacher_edit)
        return

    if message.data.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return

    magazine = data.magazine()
    if len(magazine) == 0:
        msg = bot.send_message(chat_id, 'В веденном классе нет учеников, попробуйте выбрать другой класс,'
                                        'или нажмите *Отмена* для выхода:')
        bot.register_next_step_handler(msg, teacher_edit)
        return

    ls_of_marks = data.get_grade_marks()
    bot.send_message(chat_id, ls_of_marks, parse_mode='Markdown')
    # получаем всех учеников и выводим их списком
    markup = types.InlineKeyboardMarkup()
    data.dict_of_data['magazine'] = magazine
    magazine = sorted(magazine, key=lambda x: x[7:x.find('.')])
    for i in magazine:
        markup.add(types.InlineKeyboardButton(text=i[i.find(':') + 1:], callback_data=i[:i.find(':')]))
    bot.send_message(chat_id, 'Список учеников :', reply_markup=markup)


def change_hw_or_marks(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    data.dict_of_data['grade'] = message.text
    if data.check_grade():
        msg = bot.send_message(chat_id, 'Введенный класс не сущесвует, введите заного,'
                                        ' или нажмите кнопку *Отмена*:')
        bot.register_next_step_handler(msg, change_hw_or_marks)
        return
    bot.send_message(chat_id, 'Выберите действие: ',
                     reply_markup=action())
    bot.send_message(chat_id, 'Если хотите вернуться к выбору классов, нажмите кнопку *Вернуться*',
                     reply_markup=return_markup())


def return_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Вернуться в меню'))
    return markup


def change_homework(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    # получаем все данные, а именно логин, класс, дз
    new_task = data.change_homework(message.text)
    bot.send_message(chat_id, 'Задание было успешно обновленно;\nНовое задание: \n' + new_task)
    bot.send_message(chat_id, 'Выберите действие:', reply_markup=action())


def sorts_students(x):
    return x[7]


def teacher_edit(message):
    chat_id = message.from_user.id
    try:    # если пользователь ошибся и перехотел вводить заного
        message.data.lower()
    except AttributeError:
        if message.text.lower() == data.cancel_word:
            bot.send_message(chat_id, 'Операция отменена.')
            return
        msg = bot.send_message(chat_id, 'В веденном классе нет учеников, попробуйте выбрать другой класс,'
                                        'или нажмите *Отмена* для выхода:')
        bot.register_next_step_handler(msg, teacher_edit)
        return

    if message.data.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    magazine = data.magazine()
    magazine = sorted(magazine, key=sorts_students)
    if len(magazine) == 0:
        msg = bot.send_message(chat_id, 'В веденном классе нет учеников, попробуйте выбрать другой класс,'
                                        'или нажмите *Отмена* для выхода:')
        bot.register_next_step_handler(msg, teacher_edit)
        return

    ls_of_marks = data.get_grade_marks()
    bot.send_message(chat_id, ls_of_marks, parse_mode='Markdown')
    subject = data.get_subject().capitalize() + ' : '
    # получаем всех учеников и выводим их списком
    markup = types.InlineKeyboardMarkup()
    for i in magazine:
        markup.add(types.InlineKeyboardButton(text=i[i.find(':') + 1:], callback_data=i[:i.find(':')]))
    bot.send_message(chat_id, subject, reply_markup=markup)


def accept(message):    # установка оценки,
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word or message.text == 'Введите оценку:':
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if data.set_mark(message.text):
        bot.send_message(chat_id, '{} - {}.'.format(data.dict_of_data.get('name'), message.text))
        # if data.dict_of_data.get('login').find('к') > -1:
        #     bot.send_message(chat_id, 'Выберите действие:', reply_markup=action_for_class())
        # else:
        #     bot.send_message(chat_id, 'Выберите действие:', reply_markup=action())
        markup = types.InlineKeyboardMarkup()
        for i in data.magazine():
            markup.add(types.InlineKeyboardButton(text=i[i.find(':') + 1:], callback_data=i[:i.find(':')]))
        bot.send_message(chat_id, 'Список учеников :', reply_markup=markup)
    else:
        msg = bot.send_message(chat_id, 'Оценка не установлена, введите число:')
        bot.register_next_step_handler(msg, accept)


@bot.message_handler(commands=['admin'])    # панель админа
def admin(message):
    msg = bot.send_message(message.from_user.id, 'Введите пароль:', reply_markup=cancel_key())
    bot.register_next_step_handler(msg, admin_room)


def choose():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Создать'),
               types.KeyboardButton(text='Редактировать'))
    markup.add(types.KeyboardButton(text='Импорт'),
               types.KeyboardButton(text='Экспорт'))
    return markup


def admin_room(message):
    chat_id = message.from_user.id  # ЗАЧЕМ ПАРОЛЬЬЬ???
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    if message.text != data.dict_of_admins.get(chat_id) and message.text != 'Назад в админ. меню':
        msg = bot.send_message(message.from_user.id, 'Неверный пароль.\nВведите его '
                                                     'заного или выйдите нажав кнопку *Отмена*:')
        bot.register_next_step_handler(msg, admin_room)
        return
    # если все успешно, то есть пароль ок,
    # то ты в комнате админа
    bot.send_message(chat_id, 'Выберите какое действие вы хотите совершить:', reply_markup=choose())


def pre_change_banner_or_text(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.check_ad(message.text):
        if message.text.find('картинка') > -1:
            msg = bot.send_message(chat_id, 'Перешлите новую картинку:')
            bot.register_next_step_handler(msg, change_banner)
        else:
            msg = bot.send_message(chat_id, 'Введите новый текст:')
            bot.register_next_step_handler(msg, change_banner_or_text)
    else:
        msg = bot.send_message(chat_id, 'Введенное рекламное средство не найдено,\nкликните на клавиатуру ещё раз:')
        bot.register_next_step_handler(msg, pre_change_banner_or_text)


def change_banner(message):  # установка нового банера
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    path = data.dict_of_data.get('ad') + '.jpg'
    if message.json.get('document') is None:
        if message.json.get('photo') is None:
            msg = bot.send_message(chat_id, 'Введенная фотография не подходит, отправьте новую:')
            bot.register_next_step_handler(msg, change_banner)
            return
        else:
            file_id = message.json.get('photo')[0].get('file_id')
            file_info = bot.get_file(file_id)
            with open(path, 'wb') as f:
                f.write(
                    requests.get(
                        'https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content)
    else:
        file_id = message.json.get('document').get('file_id')
        file_info = bot.get_file(file_id)
        with open(path, 'wb') as f:
            f.write(requests.get(
                'https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content)
    data.change_ad(path)
    bot.send_message(chat_id, 'Операция успешно завершена.')


def change_banner_or_text(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    data.change_ad(message.text)
    bot.send_message(chat_id, 'Операция успешно завершена.')


def days_tt():  # клавиатурка для расписания
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Пн'), types.KeyboardButton(text='Вт'))
    markup.add(types.KeyboardButton(text='Ср'), types.KeyboardButton(text='Чт'))
    markup.add(types.KeyboardButton(text='Пт'), types.KeyboardButton(text='Сб'))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def pre_change_tt(message):  # функция для ввода дня изменяемого раписанием
    chat_id = message.from_user.id
    msg = bot.send_message(chat_id, 'Кликните на день, который хотите изменить:',
                           reply_markup=days_tt())
    # выбор через клавиатурку дня для смены расписания
    bot.register_next_step_handler(msg, pre_change_tt2)


def pre_change_tt2(message):  # функция для ввода расписания
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    ls_of_days = ['Пн', 'Вт', 'Ср',
                  'Чт', 'Пт', 'Сб']
    if message.text not in ls_of_days:
        msg = bot.send_message(chat_id, 'Вы не выбрали день.\n'
                                        'Выберите день заного:',
                               reply_markup=days_tt())
        bot.register_next_step_handler(msg, pre_change_tt2)
        return
    data.dict_of_data['day'] = message.text
    msg = bot.send_message(chat_id, 'Старое расписание на {} уничтожено, '
                                    'выберите предметы для нового рассписания на этот день:'.format(data.dict_of_data.get('day')),
                           reply_markup=keyboard_of_subjects_for_admin())
    # ввод нового расписания, символ разделитель это для
    # смещение коретки на некст строку
    bot.register_next_step_handler(msg, change_tt)


def change_tt(message):  # функция на смену расписания
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        data.dict_of_data['new_timetable'] = '0'
        return
    data.set_tt(message.text)
    # установка расписания
    msg = bot.send_message(chat_id, 'Предмет добавлен в заданный день, для продолжения '
                                    'кликайте на нужный предмет, для завершения *Назад*.')
    bot.register_next_step_handler(msg, change_tt)


def studs(ls_of_stud):  # генерация кнопок студентов
    markup = types.InlineKeyboardMarkup()
    for i in ls_of_stud:
        markup.add(types.InlineKeyboardButton(text=i[:i.find(':')], callback_data=i[i.find(':') + 1:] + 'sx'))
    return markup


def pre_change_list_of_child(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    ls_of_stud = data.check_stud(message.text)
    if ls_of_stud is None:
        msg = bot.send_message(chat_id, 'Неверный код, или в классе нет учеников,'
                                        ' попробуйте ещё раз или нажмите кнопку *Отмена*:')
        bot.register_next_step_handler(msg, pre_change_list_of_child)
        return
    bot.send_message(chat_id, 'Список учеников, кликните для редактирования :',
                     reply_markup=studs(ls_of_stud))


def accept_id(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.change_id(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена.\n'
                                  'ID ученика - {}.'.format(message.text))
    else:
        msg = bot.send_message(chat_id, 'Выбранный ID не подходит, попробуйте другой, '
                                        'или нажмите кнопку *Отмена*:')
        bot.register_next_step_handler(msg, accept_id)


def buttons_of_teacher():  # клавиатурка для игры с учителем
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Сменить школу', callback_data='сш'),
               types.InlineKeyboardButton(text='Сменить id', callback_data='tid'))
    markup.add(types.InlineKeyboardButton(text='Сменить пароль', callback_data='cp'),
               types.InlineKeyboardButton(text='Сменить предмет', callback_data='sub'))
    markup.add(types.InlineKeyboardButton(text='Удалить', callback_data='td'))
    return markup


def change_id_teacher(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    try:
        info = data.check_teacher_id(message.text)[0]
    except:
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, change_id_teacher)
    else:
        data.dict_of_data['login'] = message.text   # вывод инфы о учителе
        info = list(info)
        for i in info[:-1]:
            if i is None:
                msg = bot.send_message(chat_id, 'Учитель создан неправильно, он удален, '
                                                'пересоздайте его, или же, введите новый ID:')
                data.delete_teacher()
                bot.register_next_step_handler(msg, change_id_teacher)
                return
        info[0] = 'Код школы: ' + info[0]
        info[1] = 'Код учителя: ' + info[1]
        info[2] = 'Пароль учителя: ' + info[2]
        if info[3].find('к') > -1:
            info[3] = 'Классный руководитель ' + info[3][1:] + ' класса'
        else:
            info[3] = 'Предмет учителя: ' + info[3]
        try:
            info[4] = 'Баллы учителя: ' + info[4]
        except TypeError:
            info[4] = 'Баллы учителя: 0'
        bot.send_message(chat_id, 'Данные учителя :\n' + '\n'.join(info),
                         reply_markup=buttons_of_teacher())


# далее все методы изменения учителя


def change_school_teacher(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_schoold_id(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена, новый ID школы учителя - {}.'.format(message.text))
    else:
        msg = bot.send_message(chat_id, 'Выбранный ID не подходит, введите его ещё раз,'
                                        ' или кликните на кнопку *Назад* для выхода')
        bot.register_next_step_handler(msg, change_school_teacher)


def change_teacher_id(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_id(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена, новый учительский ID - {}'.format(message.text))
    else:
        msg = bot.send_message(chat_id, 'Выбранный ID не подходит, введите его ещё раз,'
                                        ' или кликните на кнопку *Назад* для выхода')
        bot.register_next_step_handler(msg, change_teacher_id)


def change_teacher_password(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_password(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена, новый пароль - {}.'.format(message.text))
    else:
        msg = bot.send_message(chat_id, 'Пароль не может быть таким, введите другой:')
        bot.register_next_step_handler(msg, change_teacher_password)


def change_teacher_subj(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_subj(message.text):
        bot.send_message(chat_id, 'Операция успешно завершена, установленый предмет - {}.'.format(message.text))
    else:
        msg = bot.send_message(chat_id, 'Этот предмет преподает другой учитель, введите новый:')
        bot.register_next_step_handler(msg, change_teacher_subj)


def create_school(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.create_school(message.text):
        msg = bot.send_message(chat_id, 'Школа успешно созданна, введите название новой школы:')
        bot.register_next_step_handler(msg, new_title_of_school)
    else:
        msg = bot.send_message(chat_id, 'Школа с таким ID уже существует. введите другой:')
        bot.register_next_step_handler(msg, create_school)


def new_title_of_school(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_title_of_school(message.text):
        msg = bot.send_message(chat_id, 'Название школы - {} установлено,'
                                        ' введите новости школы, если нет то -1:'.format(message.text))
        bot.register_next_step_handler(msg, new_afisha_of_school)
    else:
        msg = bot.send_message(chat_id, 'Введенное название существует, попробуйте ввести другое:')
        bot.register_next_step_handler(msg, new_title_of_school)


def new_afisha_of_school(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_new_afisha(message.text):
        bot.send_message(chat_id, 'Школа успешно созданна.')
    else:
        msg = bot.send_message(chat_id, 'Введенный текст не подходит, введите новый:')
        bot.register_next_step_handler(msg, new_afisha_of_school)


def create_grade(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.check_school(message.text):  # проверка, существует ли введенная школа
        msg = bot.send_message(chat_id, 'Введите ID класса (3 символа):')
        bot.register_next_step_handler(msg, new_grade)
    else:
        msg = bot.send_message(chat_id, 'Школа с введенным ID не найдена, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, create_grade)


def new_grade(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.create_grade(message.text):
        msg = bot.send_message(chat_id, 'Класс создан, введите номер класса (5б):')
        bot.register_next_step_handler(msg, set_number)
    else:
        msg = bot.send_message(chat_id, 'Введенный ID не подходит, введите новый:')
        bot.register_next_step_handler(msg, new_grade)


def set_number(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_number(message.text):
        msg = bot.send_message(chat_id, 'Номер - {} установлен, '
                                        'пришлите фотографию классного руководителя:'.format(message.text))
        bot.register_next_step_handler(msg, set_photo)
    else:
        msg = bot.send_message(chat_id, 'Введенный номер не подходит, введите новый:')
        bot.register_next_step_handler(msg, set_number)


def set_photo(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return

    school_id, grade_id = data.dict_of_data.get('school_id'), data.dict_of_data.get('grade_id')
    path = school_id + grade_id + '.png'
    if message.json.get('document') is None:
        if message.json.get('photo') is None:
            msg = bot.send_message(chat_id, 'Введенная фотография не подходит, введите новую:')
            bot.register_next_step_handler(msg, set_photo)
            return
        else:
            file_id = message.json.get('photo')[0].get('file_id')
            file_info = bot.get_file(file_id)
            with open(path, 'wb') as f:
                f.write(
                    requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content)
    else:
        file_id = message.json.get('document').get('file_id')
        file_info = bot.get_file(file_id)
        with open(path, 'wb') as f:
            f.write(requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content)

    if data.set_photo(path):
        msg = bot.send_message(chat_id, 'Фотография установлена, введите имя классного руководителя:')
        bot.register_next_step_handler(msg, set_grade_name_teacher)
    else:
        msg = bot.send_message(chat_id, 'Введенная фотография не подходит, введите новую:')
        bot.register_next_step_handler(msg, set_photo)


def set_grade_name_teacher(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_grade_name_teacher(message.text):
        msg = bot.send_message(chat_id, 'Имя классного руководителя, а именно - {} установлено,'
                                        ' введите код беседы (если нет то -1):'.format(message.text))
        bot.register_next_step_handler(msg, set_code)
    else:
        msg = bot.send_message(chat_id, 'Введеное имя не подходит, введите новое:')
        bot.register_next_step_handler(msg, set_grade_name_teacher)


def set_code(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_code(message.text):
        msg = bot.send_message(chat_id, 'Ссылка-приглашение установлена, введите текст '
                                        'доски объявлений (если его нет, то -1):')
        bot.register_next_step_handler(msg, set_desk)
    else:
        msg = bot.send_message(chat_id, 'Введенная ссылка не подходит, введите новую или -1:')
        bot.register_next_step_handler(msg, set_code)


def keyboard_of_subjects_for_admin():   # функция дл клавиатурки на редактирование предметов
    result = data.get_all_subjects()
    if result:  # если предметы есть, заходим в меню и выводим все предметы, иначе не выводим меню, а говорим что тут пусто
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for i in result:
            markup.add(types.KeyboardButton(text=i[1]))
        markup.add(types.KeyboardButton(text=data.back_word))
        return markup
    return False


def set_desk(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_desk(message.text):
        msg = bot.send_message(chat_id, 'Доска успешно установленна.\n'
                                        'Выберите предметы которые будут выводится у учителя:',
                               reply_markup=keyboard_of_subjects_for_admin())
        bot.register_next_step_handler(msg, set_of_subject_for_class)
    else:
        msg = bot.send_message(chat_id, 'Введенная информация не подходит, введите новую:')
        bot.register_next_step_handler(msg, set_desk)


def set_of_subject_for_class(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Класс успешно создан')
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    msg = bot.send_message(chat_id, data.insert_in_grade_of_subject(message.text),
                           reply_markup=keyboard_of_subjects_for_admin())
    bot.register_next_step_handler(msg, set_of_subject_for_class)


def pre_create_stud(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.get_grade(message.text) is not None:
        msg = bot.send_message(chat_id, 'Введите имя нового ученика:')
        bot.register_next_step_handler(msg, create_stud)
    else:
        msg = bot.send_message(chat_id, 'Введенного класса не сущесвует, попробуйте заного:')
        bot.register_next_step_handler(msg, pre_create_stud)


def create_stud(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.create_stud(message.text):
        msg = bot.send_message(chat_id, 'Имя - {} установлено, введите ID нового ученика:'.format(message.text))
        bot.register_next_step_handler(msg, set_stud_id)
    else:
        msg = bot.send_message(chat_id, 'Введенное имя не подходит, введите новое:')
        bot.register_next_step_handler(msg, create_stud)


def set_stud_id(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_stud_id(message.text):
        bot.send_message(chat_id, 'Новый ученик добавлен.')
    else:
        msg = bot.send_message(chat_id, 'Введенный ID не подходит, введите новый:')
        bot.register_next_step_handler(msg, set_stud_id)


def pre_create_teach(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.get_school(message.text):
        msg = bot.send_message(chat_id, 'Введите преподовательский ID (до 4-ёх цифр):')
        bot.register_next_step_handler(msg, create_teach)
    else:
        msg = bot.send_message(chat_id, 'Школы с введенным ID не существует, попробуйте ввести ещё раз:')
        bot.register_next_step_handler(msg, pre_create_teach)


def create_teach(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.create_teach(message.text):
        msg = bot.send_message(chat_id, 'Введите пароль учителя:')
        bot.register_next_step_handler(msg, create_teacher_password)
    else:
        msg = bot.send_message(chat_id, 'Введенный ID не подходит, попробуйте снова:')
        bot.register_next_step_handler(msg, create_teach)


def create_teacher_password(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_password(message.text):
        msg = bot.send_message(chat_id, 'Введите предмет учителя:', reply_markup=keyboard_of_subjects_for_admin())
        bot.register_next_step_handler(msg, create_teacher_subj)
    else:
        msg = bot.send_message(chat_id, 'Пароль не может быть таким, введите другой:')
        bot.register_next_step_handler(msg, create_teacher_password)


def create_teacher_subj(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
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
    markup.add(types.InlineKeyboardButton(text='Удаление школы', callback_data='удлшк'))
    return markup


def pre_edit_school(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.get_school(message.text):
        bot.send_message(chat_id, 'Редактировать:', reply_markup=edit_school())
    else:
        msg = bot.send_message(chat_id, 'Школы с введенным ID не найдено, введите ещё раз ID:')
        bot.register_next_step_handler(msg, pre_edit_school)


def edit_name_of_school(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_name_of_school(message.text):
        bot.send_message(chat_id, 'Название школы успешно изменено.')
    else:
        msg = bot.send_message(chat_id, 'Введите другое название школы:')
        bot.register_next_step_handler(msg, edit_name_of_school)


def edit_news(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
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
    markup.add(types.InlineKeyboardButton(text='Ссылка-приглашение', callback_data='ссылпригл'))
    markup.add(types.InlineKeyboardButton(text='Предметы', callback_data='subjects'))
    markup.add(types.InlineKeyboardButton(text='Расписание', callback_data='ttable'))
    markup.add(types.InlineKeyboardButton(text='Удаление', callback_data='удкл'))
    return markup


def edit_grade(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.get_grade(message.text) is not None:
        bot.send_message(chat_id, 'Редактировать:', reply_markup=grade_butt())
    else:
        msg = bot.send_message(chat_id, 'Класса с введенным ID не существует, введите ID заного:')
        bot.register_next_step_handler(msg, edit_grade)


def new_number(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_number(message.text):
        bot.send_message(chat_id, 'Номер класса установлен.')
    else:
        msg = bot.send_message(chat_id, 'Новый номер класса недопустим, введите другой:')
        bot.register_next_step_handler(msg, new_number)


def photo_grade_teacher(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return

    school_id, grade_id = data.dict_of_data.get('school_id'), data.dict_of_data.get('grade_id')
    path = school_id + grade_id + '.png'
    if message.json.get('document') is None:
        if message.json.get('photo') is None:
            msg = bot.send_message(chat_id, 'Введенная фотография не подходит, введите новую:')
            bot.register_next_step_handler(msg, photo_grade_teacher)
            return
        else:
            file_id = message.json.get('photo')[0].get('file_id')
            file_info = bot.get_file(file_id)
            with open(path, 'wb') as f:
                f.write(
                    requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content)
    else:
        file_id = message.json.get('document').get('file_id')
        file_info = bot.get_file(file_id)
        with open(path, 'wb') as f:
            f.write(requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content)

    if data.set_photo(path):
        bot.send_message(chat_id, 'Фото класного руководителя установлено.')
    else:
        msg = bot.send_message(chat_id, 'Введенная фотография не подходит, введите новую:')
        bot.register_next_step_handler(msg, photo_grade_teacher)


def set_grade_name_teacher2(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_grade_name_teacher(message.text):
        msg = bot.send_message(chat_id, 'Имя классного рук. установленно.')
    else:
        msg = bot.send_message(chat_id, 'Введеное имя не подходит, введите новое:')
        bot.register_next_step_handler(msg, set_grade_name_teacher2)


def set_desk2(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_desk(message.text):
        bot.send_message(chat_id, 'Доска обновлена')
    else:
        msg = bot.send_message(chat_id, 'Введенная информация не подходит, введите новую:')
        bot.register_next_step_handler(msg, set_desk2)


def edit_admin():   # клавиатурка админа
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(types.KeyboardButton(text='Реклама'))
    markup.add(types.KeyboardButton(text='Школа'),
               types.KeyboardButton(text='Класс.'))
    markup.add(types.KeyboardButton(text='Учеников'),
               types.KeyboardButton(text='Преподователей'))
    markup.add(types.KeyboardButton(text='предмет'),
               types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def create_admin():   # клавиатурка админа на создание
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Школу'),
               types.KeyboardButton(text='Класс'))
    markup.add(types.KeyboardButton(text='Ученика'),
               types.KeyboardButton(text='Учителя'))
    markup.add(types.KeyboardButton(text='Предмет'))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def edit_baner(ls_of_buttons):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i in ls_of_buttons:
        markup.add(types.KeyboardButton(text=i))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def import_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Учеников.'), types.KeyboardButton(text='Преподователей.'))
    markup.add(types.KeyboardButton(text='Расписания'))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def import_stud(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return

    if message.json.get('document') is None:
        msg = bot.send_message(chat_id, 'Введенный файл не подходит, введите новый (для выхода нажмите кнопку *Назад*):')
        bot.register_next_step_handler(msg, import_stud)
        return

    file_id = message.json.get('document').get('file_id')
    file_info = bot.get_file(file_id)
    try:
        bot.send_message(chat_id, data.import_stud(requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content.decode('utf-8')))
    except UnicodeDecodeError:
        bot.send_message(chat_id, data.import_stud(requests.get(
            'https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content.decode(
            'cp1251')))


def import_teach(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return

    if message.json.get('document') is None:
        msg = bot.send_message(chat_id, 'Введенный файл не подходит, введите новый (для выхода нажмите кнопку *Назад*):')
        bot.register_next_step_handler(msg, import_teach)
        return

    file_id = message.json.get('document').get('file_id')
    file_info = bot.get_file(file_id)
    try:
        bot.send_message(chat_id, data.import_teach(requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content.decode('utf-8')))
    except UnicodeDecodeError:
        bot.send_message(chat_id, data.import_teach(requests.get(
            'https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content.decode(
            'cp1251')))


def import_timetable(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return

    if message.json.get('document') is None:
        msg = bot.send_message(chat_id,
                               'Введенный файл не подходит, введите новый (для выхода нажмите кнопку *Назад*):')
        bot.register_next_step_handler(msg, import_timetable)
        return

    file_id = message.json.get('document').get('file_id')
    file_info = bot.get_file(file_id)
    try:
        bot.send_message(chat_id, data.import_timetable(
            requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content.decode(
                'cp1251')))
    except UnicodeDecodeError:
        bot.send_message(chat_id, data.import_timetable(
            requests.get(
                'https://api.telegram.org/file/bot{0}/{1}'.format(data.TOKEN, file_info.file_path)).content.decode(
                'utf-8')))


def export_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(types.KeyboardButton(text='учеников'), types.KeyboardButton(text='учителей'))
    markup.add(types.KeyboardButton(text='предметов'), types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def pre_export_students(message):
    chat_id = message.from_user.id
    bot.send_message(chat_id, 'Доступные школы , их ID:\n' + data.get_list_of_schoold_for_admin())
    msg = bot.send_message(chat_id, 'Введите ID школы, из которой хотите экспортировать студентов:')
    bot.register_next_step_handler(msg, export_students)


def export_students(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.get_school_for_export(message.text):
        msg = bot.send_message(chat_id, 'Школа не найдена, попбробуйте ещё раз или нажмите *Назад*:')
        bot.register_next_step_handler(msg, export_students)
        return
    data.export_students()  # создаем файл
    with open('temp_file.txt', 'rb') as f:
        bot.send_document(chat_id, f)  # отсылаем его
    os.remove('temp_file.txt')  # удаляем его


def export_teachers(message):
    chat_id = message.from_user.id

    data.export_teachers()  # создаем файл
    with open('temp_file.txt', 'rb') as f:
        bot.send_document(chat_id, f)  # отсылаем его
    os.remove('temp_file.txt')  # удаляем его


def create_subject(message):        # создание предмета
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    result = data.create_subject(message.text.capitalize())  # добавляем предмет в базу + увеличиваем первую букву
    bot.register_next_step_handler(bot.send_message(chat_id, result), create_subject)


def pre_edit_subject(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    for i in data.get_all_subjects():
        if i[1] == message.text:
            data.dict_of_data['old_subject'] = message.text
            bot.register_next_step_handler(bot.send_message(chat_id, "Введите новое название предмета "
                                                                     "(-1 если хотите его удалить):"), edit_subject)
            return
    else:
        bot.register_next_step_handler(bot.send_message(chat_id, "Введенный предмет не найден, попробуйте ещё раз:"),
                                       pre_edit_subject)


def edit_subject(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    result = data.edit_subject(message.text.capitalize())  # редактируем предмет
    if result.find('введите') > -1:
        bot.register_next_step_handler(bot.send_message(chat_id, result), edit_subject)
    else:
        bot.register_next_step_handler(bot.send_message(chat_id, result), pre_edit_subject)


def pre_edit_url_of_invite(message):
    chat_id = message.from_user.id
    result = data.get_info_about_grade()
    msg = bot.send_message(chat_id, result)
    bot.register_next_step_handler(msg, edit_url_of_invite)


def edit_url_of_invite(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return

    if data.set_code(message.text):
        bot.send_message(chat_id, 'Ссылка успешно обновлена')
    else:
        bot.register_next_step_handler(bot.send_message(chat_id, 'Ссылка не удовлетворяет '
                                                                 'стандартам, введите новую ссылку:'),
                                       edit_url_of_invite)


def export_subjects(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    subjects = data.export_subjects(message.text)
    if subjects:
        subjects = [x[0] for x in subjects]
        subjects = '\n'.join(subjects)
        with open('subjects.txt', 'w') as f:
            f.write(subjects)
        with open('subjects.txt', 'rb') as f:
            bot.send_document(chat_id, f)
        os.remove('subjects.txt')
    else:
        bot.register_next_step_handler(bot.send_message(chat_id, 'Введенного класса не существует,'
                                                                 ' или у него нет предметов,'
                                                                 ' введите заного или назад:'),
                                       export_subjects)


def keyboard_of_edit_subjects_grade():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Добавить'), types.KeyboardButton(text='Удалить'))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def edit_subject_in_class(message):
    chat_id = message.from_user.id
    res = data.write_class_for_edit_subject()
    if res.find('хотите') > -1:
        bot.send_message(chat_id, res, reply_markup=keyboard_of_edit_subjects_grade())
    else:
        msg = bot.send_message(chat_id, 'Предметов в заданном классе нет;\nВыберите какой предмет хотите добавить:',
                               reply_markup=keyboard_of_subjects_for_admin())
        bot.register_next_step_handler(msg, add_subject_in_grade)


def add_subject_in_grade(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    msg = bot.send_message(chat_id, data.add_subject_in_grade(message.text))
    bot.register_next_step_handler(msg, add_subject_in_grade)


def keyboard_of_subjects_for_delete():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    for i in data.export_subjects(data.dict_of_data.get('school_id') + data.dict_of_data.get('grade_id')):
        markup.add(types.KeyboardButton(text=i[0]))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def remove_subject_in_grade(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    data.remove_subject_in_grade(message.text)
    bot.register_next_step_handler(bot.send_message(chat_id, 'Предмет удален, если хотите продолжить, '
                                                             'вводите предметы или жмите *Назад*'), remove_subject_in_grade)


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.', reply_markup=choose())
        return
    text = message.text
    if text == '📆Расписание на завтра':
        timetable = data.get_timetable_on_tomorrow()
        bot.send_message(chat_id, timetable, parse_mode='Markdown')

    elif text == '🗓Расписание по дням':
        bot.send_message(chat_id, data.get_all_timetable())

    elif text == '📋Доска объявлений':
        bot.send_message(chat_id, data.get_desk())

    elif text == '💬Чат':
        url = data.get_invite_url()
        if url.find('t.me') > -1:
            url = 'Ссылка-приглашение:\n' + url
        bot.send_message(chat_id, url)
        return

    elif text == '📰Афиша, новости':
        afisha = data.get_afisha()
        if afisha == '-1':
            afisha = 'Новостей пока нет.'
        bot.send_message(chat_id, afisha)

    elif text == '📖Домашнее задание':
        bot.send_message(chat_id, data.print_hw())

    elif text == 'Оценки':
        if data.dict_of_data.get('school_id') == '0' or data.dict_of_data.get('grade_id') == '0':
            bot.send_message(chat_id, 'Перезайдите пожалуйста (/start)')
            return
        if data.dict_of_data.get('student') != '0':
            person_room(message)
            return
        msg = bot.send_message(chat_id, 'Введите персональный код ученика (6 символов):')
        bot.register_next_step_handler(msg, person_room)

    password = data.check_password_of_teachers()
    if data.check_password_of_teachers() is not False:
        if text == 'Вернуться в меню':
            message.text = password
            teacher_room(message)
            return

    if chat_id not in data.dict_of_admins.keys():   # далее проход только админам
        return

    if message.text.lower() == data.back_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return

    elif text == 'Создать':     # меню создания
        bot.send_message(chat_id, 'Выберите что именно вы хотите создать:', reply_markup=create_admin())

    elif text == 'Школу':   # создание школы
        msg = bot.send_message(chat_id, 'Введите ID новой школы (3 символа):')
        bot.register_next_step_handler(msg, create_school)

    elif text == 'Класс':   # создание класса
        bot.send_message(chat_id, 'Доступные школы , их ID:\n' + data.get_list_of_schoold_for_admin())
        msg = bot.send_message(chat_id, 'Введите ID школы, в которой будет этот класс (3 символа):')
        bot.register_next_step_handler(msg, create_grade)

    elif text == 'Ученика':  # создание ученика
        bot.send_message(chat_id, 'Доступные школы, Название, ID класса:\n' + data.get_list_of_grades_for_admin())
        msg = bot.send_message(chat_id, 'Введите ID класса, в который хотите добавить ученика:')
        bot.register_next_step_handler(msg, pre_create_stud)

    elif text == 'Учителя':  # создание учителя
        bot.send_message(chat_id, 'Доступные школы , их ID:\n' + data.get_list_of_schoold_for_admin())
        msg = bot.send_message(chat_id, 'Введите ID школы, в которую добавить учителя:')
        bot.register_next_step_handler(msg, pre_create_teach)

    elif text == 'Назад в админ. меню':   # возврат в комнату выбора между создать и редачить
        admin_room(message)
        return

    elif text == 'Редактировать':
        bot.send_message(chat_id, 'Выберите что хотите редактировать, '
                                  'все возможные варианты представлены на клавиатуре ниже:',
                         reply_markup=edit_admin())

    # ДАЛЕЕ ПОШЛО РЕДАКТИРОВАНИЕ

    elif text == 'Реклама':
        ls_of_data = data.get_ad()
        ls_of_buttons = []
        msg = ''
        for i in ls_of_data:
            if i[0].find('картинка') > -1:
                with open(i[1], 'rb') as f:
                    bot.send_photo(chat_id, f.read())
                msg = bot.send_message(chat_id, '👆 ' + i[0])
            else:
                bot.send_message(chat_id, i[1])
                msg = bot.send_message(chat_id, '👆  ' + i[0])
            ls_of_buttons.append(i[0])
        bot.send_message(chat_id, 'Прочтите информацию выше и выберите из панели внизу что хотите редактировать:',
                         reply_markup=edit_baner(ls_of_buttons))
        bot.register_next_step_handler(msg, pre_change_banner_or_text)

    elif text == 'Школа':
        bot.send_message(chat_id, 'Доступные школы , их ID:\n' + data.get_list_of_schoold_for_admin())
        msg = bot.send_message(chat_id, 'Введите ID школы которую хотите отредактировать (3 символа):')
        bot.register_next_step_handler(msg, pre_edit_school)

    elif text == 'Класс.':
        bot.send_message(chat_id, 'Доступные школы, Название, ID класса:\n' + data.get_list_of_grades_for_admin())
        msg = bot.send_message(chat_id, 'Введите ID класса которого вы хотите редактировать (6 символов):')
        bot.register_next_step_handler(msg, edit_grade)

    elif text == 'Учеников':    # редактировать учеников класса
        bot.send_message(chat_id, 'Доступные школы, Название, ID класса:\n' + data.get_list_of_grades_for_admin())
        msg = bot.send_message(chat_id, 'Введите код класса (6 символов):')
        bot.register_next_step_handler(msg, pre_change_list_of_child)

    elif text == 'Преподователей':
        bot.send_message(chat_id, 'Доступные школы , их ID:\n' + data.get_list_of_schoold_for_admin())
        msg = bot.send_message(chat_id, 'Введите код преподователя (до 7-и символов),'
                                        ' который хотите изменить:')
        bot.register_next_step_handler(msg, change_id_teacher)

    elif text == 'Импорт':
        bot.send_message(chat_id, 'Выберите что вы хотите импортировать нажав на соответствующую кнопку:',
                         reply_markup=import_menu())

    elif text == 'Учеников.':
        msg = bot.send_message(chat_id, 'Перенесите в чат текстовый файл с учениками')
        bot.register_next_step_handler(msg, import_stud)

    elif text == 'Преподователей.':
        msg = bot.send_message(chat_id, 'Перенесите в чат текстовый файл с преподователями')
        bot.register_next_step_handler(msg, import_teach)

    elif text == 'Расписания':
        msg = bot.send_message(chat_id, 'Перенесите в чат текстовый файл с расписанием')
        bot.register_next_step_handler(msg, import_timetable)

    elif text == 'Экспорт':
        bot.send_message(chat_id, 'Выберите кого экспортировать:', reply_markup=export_menu())

    elif text == 'учеников':
        pre_export_students(message)

    elif text == 'учителей':
        export_teachers(message)

    elif text == 'Предмет':
        msg = bot.send_message(chat_id, 'Введите предмет который хотите добавить:')
        bot.register_next_step_handler(msg, create_subject)

    elif text == 'предмет':
        if keyboard_of_subjects_for_admin() is False:
            bot.send_message(chat_id, 'Нет предметов для редактирования.')
            return
        msg = bot.send_message(chat_id, 'Введите предмет который хотите редактировать:', reply_markup=keyboard_of_subjects_for_admin())
        bot.register_next_step_handler(msg, pre_edit_subject)

    elif text == 'предметов':
        bot.send_message(chat_id, 'Доступные школы, Название, ID класса:\n' + data.get_list_of_grades_for_admin())
        bot.register_next_step_handler(bot.send_message(chat_id, 'Введите класс предметы которого хотите импортировать:'),
                                       export_subjects)

    elif text == 'Добавить':
        msg = bot.send_message(chat_id, 'Выберите какой предмет хотите добавить:',
                               reply_markup=keyboard_of_subjects_for_admin())
        bot.register_next_step_handler(msg, add_subject_in_grade)

    elif text == 'Удалить':
        msg = bot.send_message(chat_id, 'Выберите какой предмет хотите удалить:',
                               reply_markup=keyboard_of_subjects_for_delete())
        bot.register_next_step_handler(msg, remove_subject_in_grade)


if __name__ == '__main__':
    if datetime.datetime.now().strftime('%a, %H:%M') == 'Mon, 05:00':  # чтоб чистило оценки каждый понедельник в 5 утра ПО ВРЕМЕНИ СЕРВЕРА
        data.clear_marks()
    bot.infinity_polling(True)
