import time
import requests
import telebot
from telebot import types
import datetime
import data


bot = telebot.TeleBot(data.TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.from_user.id
    with open(data.get_res('картинка1'), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('реклама1'))  # получение текста рекламы
    bot.send_message(chat_id, data.get_list_of_schools())
    # получение всех школ участвующих в проекте
    msg = bot.send_message(chat_id, 'Введите индивидуальный код класса (до 6-ти символов):', reply_markup=cancel_key())
    bot.register_next_step_handler(msg, second_step)


def board():
    # метод для кнопок на 2-ой форме,
    # каждая кнопка имеет свое id для метода
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    first_button = types.KeyboardButton(text='📆Расписание на завтра')
    second_button = types.KeyboardButton(text='🗓Расписание по дням')
    markup.add(first_button, second_button)
    third_button = types.KeyboardButton(text='📋Доска объявлений')
    fourth_button = types.KeyboardButton(text='💬Классный чат')
    markup.add(third_button, fourth_button)
    markup.add(types.KeyboardButton(text='📰Афиша, новости'),
               types.KeyboardButton(text='📖Домашнее задание'))
    markup.add(types.KeyboardButton(text='🚪Личный кабинет'),
               types.KeyboardButton(text='◀️Отмена'))
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
    with open(data.get_res('картинка2'), 'rb') as f:
        bot.send_photo(chat_id, f.read())  # получение второго банера рекламы
    bot.send_message(chat_id, data.get_res('реклама2'))  # получение второго текста рекламы

    grade = data.get_grade(message.text)  # получаем всю информацию о классе для формы
    if grade is None:   # если школа не найдена
        msg = bot.send_message(chat_id, 'Неверный код, попробуйте'
                                        ' ещё раз(или нажмите кнопку *Отмена*):', reply_markup=cancel_key())
        bot.register_next_step_handler(msg, second_step)
        return
    time.sleep(3)
    with open(grade[0][3], 'rb') as f:
        photo = f.read()  # получение фото классного руковод.
        bot.send_photo(chat_id, photo)
    name_of_day = data.trans(datetime.datetime.now().strftime("%A"), '\n'.join(grade[1]))
    name_of_day, timetable = name_of_day[:name_of_day.find('\n')], name_of_day[name_of_day.find('\n'):]
    bot.send_message(chat_id,
                     'Классный руководитель:\n' + grade[0][4] +
                     f'\n\nРасписание на {name_of_day} {datetime.datetime.now().strftime("%d.%m.%Y")}:' + timetable,
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
        msg = bot.send_message(chat_id, 'Введите домашнее задание:')
        bot.register_next_step_handler(msg, change_homework)

    elif obj.data == 'ro':  # выбор дз для изменения
        teacher_edit(obj)

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
        data.dict_of_data['last_stud_id'] = obj.data
        msg = bot.send_message(chat_id, 'Введите оценку:')
        bot.register_next_step_handler(msg, accept)


def person_room(message):   # комната школьника
    chat_id = message.from_user.id
    if message.text.lower().find('отмена') > -1:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    marks = data.get_marks(data.dict_of_data.get('school_id') + data.dict_of_data.get('grade_id') + message.text)
    # если код неверен выходим, если верен выводим оценки
    if marks is None:
        msg = bot.send_message(message.from_user.id, 'Неверный код, или у ученика нет оценок, '
                                                     'попробуйте ещё раз или нажмите кнопку "Отмена" для выхода:')
        bot.register_next_step_handler(msg, person_room)
        return
    bot.send_message(chat_id, marks)   # выводим оценки


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
        markup.add(types.KeyboardButton(text=i[0]))
    markup.add(types.KeyboardButton(text='Отмена'))
    return markup


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
        msg = bot.send_message(chat_id, 'Введенный класс не сущесвует, введите заного,'
                                        ' или нажмите кнопку *Отмена*:')
        bot.register_next_step_handler(msg, change_hw_or_marks)
        return
    bot.send_message(chat_id, 'Выберите действие: ',
                     reply_markup=action())


def change_homework(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    # получаем все данные, а именно логин, класс, дз
    new_task = data.change_homework(message.text)
    bot.send_message(chat_id, 'Задание было успешно обновленно;\nНовое задание: \n' + new_task)


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
    if len(magazine) == 0:
        msg = bot.send_message(chat_id, 'В веденном классе нет учеников, попробуйте выбрать другой класс,'
                                        'или нажмите *Отмена* для выхода:')
        bot.register_next_step_handler(msg, teacher_edit)
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
    if data.set_mark(message.text):
        bot.send_message(chat_id, 'Оценка успешно установлена.')
    else:
        msg = bot.send_message(chat_id, 'Оценка не установлена, ввидите число:')
        bot.register_next_step_handler(msg, accept)


@bot.message_handler(commands=['admin'])    # панель админа
def admin(message):
    msg = bot.send_message(message.from_user.id, 'Введите пароль:', reply_markup=cancel_key())
    bot.register_next_step_handler(msg, admin_room)


def choose():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Создать'),
               types.KeyboardButton(text='Редактировать'))
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
    path = 'img\\' + data.dict_of_data.get('ad') + '.jpg'
    if message.json.get('document') is None:
        if message.json.get('photo') is None:
            msg = bot.send_message(chat_id, 'Введенная фотография не подходит, введите новую:')
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
    markup.add(types.KeyboardButton(text='Понедельник'), types.KeyboardButton(text='Вторник'))
    markup.add(types.KeyboardButton(text='Среда'), types.KeyboardButton(text='Четверг'))
    markup.add(types.KeyboardButton(text='Пятница'), types.KeyboardButton(text='Суббота'))
    markup.add(types.KeyboardButton(text='Отмена'),
               types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def pre_change_tt(message):  # функция для ввода дня изменяемого раписанием
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
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
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    ls_of_days = ['Понедельник', 'Вторник', 'Среда',
                  'Четверг', 'Пятница', 'Суббота']
    if message.text not in ls_of_days:
        msg = bot.send_message(chat_id, 'Вы не выбрали день.\n'
                                        'Выберите день заного:',
                               reply_markup=days_tt())
        bot.register_next_step_handler(msg, pre_change_tt2)
        return
    msg = bot.send_message(chat_id, 'Введите новое '
                                    'расписание (символ-разделитель - ;)\nПример:\nВы вводите: '
                                    'Русский язык;Математика ;\n'
                                    'Вывелось:\nРусский язык\nМатематика:')
    # ввод нового расписания, символ разделитель это для
    # смещение коретки на некст строку
    bot.register_next_step_handler(msg, change_tt)


def change_tt(message):  # функция на смену расписания
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    temp_message = bot.forward_message(chat_id, chat_id, message.message_id - 2)
    day = temp_message.text
    bot.delete_message(chat_id, temp_message.message_id)
    data.set_tt(message.text, day)
    # установка расписания
    msg = bot.send_message(chat_id, 'Операция успешно завершена, вы можете продолжить'
                                    ' обновлять раписание.')
    bot.register_next_step_handler(msg, pre_change_tt2)


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
                                        ' попробуйте ещё раз или нажмите кнопку *Назад*:')
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
        bot.send_message(chat_id, f'Операция успешно завершена.\n'
                                  f'ID ученика - {message.text}.')
    else:
        msg = bot.send_message(chat_id, 'Выбранный ID не подходит, попробуйте другой, '
                                        'или нажмите кнопку *Назад*:')
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
        info[0] = 'Код школы: ' + info[0]
        info[1] = 'Код учителя: ' + info[1]
        info[2] = 'Пароль учителя: ' + info[2]
        info[3] = 'Предмет учителя: ' + info[3]
        info[4] = 'Баллы учителя: ' + info[4]
        bot.send_message(chat_id, 'Данные учителя :\n' + '\n'.join(info),
                         reply_markup=buttons_of_teacher())


# далее все методы изменения учителя


def change_school_teacher(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_schoold_id(message.text):
        bot.send_message(chat_id, f'Операция успешно завершена, новый ID школы учителя - {message.text}.')
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
        bot.send_message(chat_id, f'Операция успешно завершена, новый учительский ID - {message.text}')
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
        bot.send_message(chat_id, f'Операция успешно завершена, новый пароль - {message.text}.')
    else:
        msg = bot.send_message(chat_id, 'Пароль не может быть таким, введите другой:')
        bot.register_next_step_handler(msg, change_teacher_password)


def change_teacher_subj(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.new_teacher_subj(message.text):
        bot.send_message(chat_id, f'Операция успешно завершена, установленый предмет - {message.text}.')
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
        msg = bot.send_message(chat_id, 'Введенный ID не подходит, попробуйте ещё раз:')
        bot.register_next_step_handler(msg, create_school)


def new_title_of_school(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_title_of_school(message.text):
        msg = bot.send_message(chat_id, f'Название школы - {message.text} установлено,'
                                        f' введите новости школы, если нет то -1:')
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
        msg = bot.send_message(chat_id, 'Введите ID класса(до 3-ёх символов, '
                                        'желательный шифр - год поступления + буква,'
                                        'пример 19б или же без буквы, 190):')
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
        msg = bot.send_message(chat_id, f'Номер - {message.text} установлен, '
                                        f'пришлите фотографию классного руководителя:')
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
    path = 'img\\' + school_id + grade_id + '.png'
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
        msg = bot.send_message(chat_id, f'Имя классного руководителя, а именно - {message.text} установлено,'
                                        ' введите код беседы (если нет то -1):')
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


def set_desk(message):
    chat_id = message.from_user.id
    if message.text == data.back_word:
        bot.send_message(chat_id, 'Вы вернулись в админ. панель:', reply_markup=choose())
        return
    if data.set_desk(message.text):
        bot.send_message(chat_id, 'Класс успешно создан')
    else:
        msg = bot.send_message(chat_id, 'Введенная информация не подходит, введите новую:')
        bot.register_next_step_handler(msg, set_desk)


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
        msg = bot.send_message(chat_id, f'Имя - {message.text} установлено, введите ID нового ученика:')
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
        msg = bot.send_message(chat_id, 'Введите преподовательский ID:')
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
        msg = bot.send_message(chat_id, 'Введите предмет учителя:')
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
        msg = bot.send_message(chat_id, 'Школы с введенным id не найдено, введите ещё раз id:')
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
    path = 'img\\' + school_id + grade_id + '.png'
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
        bot.register_next_step_handler(msg, set_desk)


def edit_admin():   # клавиатурка админа
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Реклама'))
    markup.add(types.KeyboardButton(text='Школа'),
               types.KeyboardButton(text='Класс.'))
    markup.add(types.KeyboardButton(text='Расписание'))
    markup.add(types.KeyboardButton(text='Учеников'),
               types.KeyboardButton(text='Преподователей'))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def create_admin():   # клавиатурка админа на создание
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Школу'),
               types.KeyboardButton(text='Класс'))
    markup.add(types.KeyboardButton(text='Ученика'),
               types.KeyboardButton(text='Учителя'))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


def edit_baner(ls_of_buttons):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i in ls_of_buttons:
        markup.add(types.KeyboardButton(text=i))
    markup.add(types.KeyboardButton(text='Назад в админ. меню'))
    return markup


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.from_user.id
    if message.text.lower() == data.cancel_word:
        bot.send_message(chat_id, 'Операция отменена.')
        return
    text = message.text
    if text == '📆Расписание на завтра':
        timetable = data.get_timetable_on_tomorrow()
        bot.send_message(chat_id, timetable)

    elif text == '🗓Расписание по дням':
        bot.send_message(chat_id, data.get_all_timetable())

    elif text == '📋Доска объявлений':
        bot.send_message(chat_id, data.get_desk())

    elif text == '💬Классный чат':
        bot.send_message(chat_id, 'Ссылка-приглошение:\n' + data.get_invite_url())
        return

    elif text == '📰Афиша, новости':
        bot.send_message(chat_id, data.get_afisha())

    elif text == '📖Домашнее задание':
        bot.send_message(chat_id, data.print_hw())

    elif text == '🚪Личный кабинет':
        msg = bot.send_message(chat_id, 'Введите персональный код ученика (до 3-ёх символов):')
        bot.register_next_step_handler(msg, person_room)

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
                                  'все возмодные варианты представлены на клавиатуре ниже:',
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
                msg = bot.send_message(chat_id, 'Чтобы редактировать картинку выше, введите ' + i[0])
            else:
                bot.send_message(chat_id, i[1])
                msg = bot.send_message(chat_id, 'Чтобы редактировать надпись выше, введите ' + i[0])
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

    elif text == 'Расписание':  # редактировать подневно расписание
        bot.send_message(chat_id, 'Доступные школы, Название, ID класса:\n' + data.get_list_of_grades_for_admin())
        msg = bot.send_message(chat_id, 'Введите код класса (6 символов):')
        bot.register_next_step_handler(msg, pre_change_tt)

    elif text == 'Учеников':    # редактировать учеников класса
        bot.send_message(chat_id, 'Доступные школы, Название, ID класса:\n' + data.get_list_of_grades_for_admin())
        msg = bot.send_message(chat_id, 'Введите код класса (6 символов):')
        bot.register_next_step_handler(msg, pre_change_list_of_child)

    elif text == 'Преподователей':
        bot.send_message(chat_id, 'Доступные школы , их ID:\n' + data.get_list_of_schoold_for_admin())
        msg = bot.send_message(chat_id, 'Введите код преподователя (до 7-и символов),'
                                        ' который хотите изменить:')
        bot.register_next_step_handler(msg, change_id_teacher)


if __name__ == '__main__':
    bot.infinity_polling(True)
