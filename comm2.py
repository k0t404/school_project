import telebot
import datetime
from con2 import BOT_TOKEN
from telebot import types
from data import db_session
from data.lessons import Lessons
from data.users import User
from data.changes import Changes
from data.keys import Keys
bot = telebot.TeleBot(BOT_TOKEN)


class KeyboardData:
    def __init__(self):
        self.user_id = ''
        self.class_to_work = ''
        self.day = ''
        self.lesson_pos = ''
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.classes = None


    def create_classes(self):
        db_session.global_init("db/logs.db")
        db_sess = db_session.create_session()
        lessons = db_sess.query(Lessons)
        classes = {'5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
        for thing in lessons:
            class_name = thing.class_letter
            if class_name not in classes[class_name.split()[0]]:
                classes[class_name.split()[0]].append(class_name)
        return classes


def gen_markup(options, key):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    for option in options:
        markup.add(types.InlineKeyboardButton(option, callback_data=f"{key}_{str(option)}"))
    return markup


def unpack(swl_thing):
    info = []
    for row in swl_thing:
        info.append(row)
    return info


def start_keyboard(user_pass):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    if user_pass == 'завуч':
        btn1 = types.KeyboardButton('Памятка')
        btn2 = types.KeyboardButton('Расписание')
        btn3 = types.KeyboardButton('Изменить расписание')
        btn4 = types.KeyboardButton('Отправить сообщение классу')
        btn5 = types.KeyboardButton('Задать вопрос')
        btn6 = types.KeyboardButton('Поиск класса')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    elif user_pass == 'учитель':
        btn1 = types.KeyboardButton('Памятка')
        btn2 = types.KeyboardButton('Расписание')
        btn3 = types.KeyboardButton('Отправить сообщение классу')
        btn4 = types.KeyboardButton('Задать вопрос')
        btn5 = types.KeyboardButton('Поиск класса')
        markup.add(btn1, btn2, btn3, btn4, btn5)
    elif user_pass == 'ученик':
        btn1 = types.KeyboardButton('Памятка')
        btn2 = types.KeyboardButton('Расписание')
        btn3 = types.KeyboardButton('Задать вопрос')
        btn4 = types.KeyboardButton('Поиск класса')
        markup.add(btn1, btn2, btn3, btn4)
    return markup


def starts(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Авторизоваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я бот Артем, и я помогу тебе с расписанием!",
                     reply_markup=markup)


def redo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Авторизоваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Давай по новой",
                     reply_markup=markup)


def search(message):
    bot.send_message(message.from_user.id, 'Выберите действие')


def question(message):
    bot.send_message(message.from_user.id, "Все вопросы можно писать на нашу почту")
    bot.send_message(message.from_user.id, "cot5626@mail.ru")


def helper(message):
    bot.send_message(message.from_user.id, "Я бот Артем.")
    bot.send_message(message.from_user.id, "Я могу:")
    bot.send_message(message.from_user.id, "Вывести расписание на сегодня")
    bot.send_message(message.from_user.id, "Внести изменения в расписание класса")
    bot.send_message(message.from_user.id, "Отправить сообщение классу")
    bot.send_message(message.from_user.id, "Напишите /quit, чтобы выйти из базы данных пользователей")
    bot.send_message(message.from_user.id, "Напишите /start, чтобы начать авторизацию по новой")
    bot.send_message(message.from_user.id, "Напишите /help, чтобы увидеть это же сообщение")
    bot.send_message(message.from_user.id, "При неправильном вводе повторяйте весь процесс заново, не надо отправлять сообщения несколько раз")


def prep_raspisanie(message):
    clas = ''.join(message.text.upper().split())
    clas = [clas[:-1], clas[-1]]
    raspisanie(message, clas)


def raspisanie(message, clas=None, autharized_student=False):
    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']

    db_sess = db_session.create_session()
    user_back = db_sess.query(User).filter(User.user_id == message.from_user.id).first()
    print(user_back.about)

    if autharized_student:
        clas = clas
    else:
        clas = f'{clas[0]} "{clas[1].capitalize()}" класс'

    if datetime.datetime.today().weekday() > 4:
        bot.send_message(message.from_user.id, 'Бот отказывается работать в выходные. Иди к МЭШ-у')
    else:
        date = days[datetime.datetime.today().weekday()]
        db_sess = db_session.create_session()
        lessons = []
        changes_made = db_sess.query(Changes).filter(Changes.class_letter == clas, Changes.day == date)
        all_changes = {}
        for change in changes_made:
            all_changes[change.lesson_pos] = change
        for row in db_sess.query(Lessons).filter(Lessons.class_letter == clas, Lessons.day == date):
            lesson = []
            if row.lesson_pos in all_changes.keys():
                lesson = [all_changes[row.lesson_pos].lesson_pos, all_changes[row.lesson_pos].lesson,
                          all_changes[row.lesson_pos].cabinet]
            else:
                lesson = [row.lesson_pos, row.lesson, row.cabinet]
            lessons.append(lesson)
        if lessons:
            bot.send_message(message.from_user.id, f'Расписание для {clas} на {date.lower()}',
                             reply_markup=start_keyboard(user_back.about))
            for row in lessons:
                if None not in row:
                    bot.send_message(message.from_user.id, '       '.join(row))
        else:
            bot.send_message(message.from_user.id, 'Такой класс не был найден, попробуй снова')


def prep_raspisanie_control(message):
    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
    date = message.text.upper().split()[0]
    if date not in days:
        bot.send_message(message.from_user.id, 'неверно введен день недели. Повторите процесс заново')
    clas = ''.join(message.text.upper().split()[1:])
    clas = [clas[:-1], clas[-1]]
    raspisanie_control(message, clas, date)


def raspisanie_control(message, clas, date):
    clas = f'{clas[0]} "{clas[1].capitalize()}" класс'

    db_sess = db_session.create_session()
    lessons = []
    changes_made = db_sess.query(Changes).filter(Changes.class_letter == clas, Changes.day == date)
    all_changes = {}

    user_back = db_sess.query(User).filter(User.user_id == message.from_user.id).first()
    print(user_back.about)
    for change in changes_made:
        all_changes[change.lesson_pos] = change
    for row in db_sess.query(Lessons).filter(Lessons.class_letter == clas, Lessons.day == date).distinct():
        lesson = []
        if row.lesson_pos in all_changes.keys():
            lesson = [all_changes[row.lesson_pos].lesson_pos, all_changes[row.lesson_pos].lesson,
                      all_changes[row.lesson_pos].cabinet]
        else:
            lesson = [row.lesson_pos, row.lesson, row.cabinet]
        lessons.append(lesson)
    if lessons:
        bot.send_message(message.from_user.id, f'Расписание для {clas} на {date.lower()}',
                         reply_markup=start_keyboard(user_back.about))
        for row in lessons:
            if None not in row:
                bot.send_message(message.from_user.id, '       '.join(row))
    else:
        bot.send_message(message.from_user.id, 'Такой класс не был найден, попробуй снова')


def prep_poisk(message):
    clas = ''.join(message.text.upper().split())
    poisk(clas, message)


def poisk(clas, message):
    db_sess = db_session.create_session()
    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
    if datetime.datetime.today().weekday() > 4:
        bot.send_message(message.from_user.id, 'В выходные невозможно найти класс')
    else:
        date = days[datetime.datetime.today().weekday()]
        clas = f'{clas[:2]} "{clas[-1]}" класс'
        print(clas)
        if str(datetime.time.hour) >= '15' and str(datetime.time.minute) >= '15':
            bot.send_message(message.from_user.id, 'Уроки уже закончились')
        else:
            if str(datetime.time.hour) >= '8' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '9'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '1'
            elif str(datetime.time.hour) >= '9' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '10'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '2'
            elif str(datetime.time.hour) >= '10' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '11'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '3'
            elif str(datetime.time.hour) >= '11' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '12'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '4'
            elif str(datetime.time.hour) >= '12' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '13'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '5'
            elif str(datetime.time.hour) >= '13' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '14'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '6'
            elif str(datetime.time.hour) >= '14' and str(datetime.time.minute) >= '15' and str(datetime.time.hour) <= '15'\
                    and str(datetime.time.minute) <= '15':
                lesson_pos = '7'
            lesson = db_sess.query(Lessons).filter(Lessons.class_letter == clas, Lessons.day == date, Lessons.lesson_pos == lesson_pos)
            row = db_sess.query(Changes).filter(Changes.day == date, Changes.lesson_pos == lesson_pos, Changes.class_letter == clas)
            if row:
                bot.send_message(message.from_user.id, f'{clas} находиться в {row.cabinet} кабинете')
            elif lesson:
                bot.send_message(message.from_user.id, f'{clas} находиться в {lesson.cabinet} кабинете')
            else:
                bot.send_message(message.from_user.id, 'Такой класс не был найден, попробуй снова')


def authorization(message, student=False):
    db_sess = db_session.create_session()
    user = User()
    if student:
        clas = message[1]
        user_id = message[0]
        user.user_id = user_id
        user.about = 'ученик'
        user.user_key = clas
        usero = user.about
        db_sess.add(user)
        db_sess.commit()
        bot.send_message(user_id, 'готово', reply_markup=start_keyboard(usero))
    else:
        check = True
        user.user_id = message.from_user.id
        key = db_sess.query(Keys).filter(Keys.key_available == message.text)
        if unpack(key) and len(message.text) == 9:
            user.about = 'завуч'
            user.user_key = message.text
        elif unpack(key) and len(message.text) == 7:
            user.about = 'учитель'
            user.user_key = message.text
        else:
            check = False
        if check:
            usero = user.about
            db_sess.add(user)
            db_sess.commit()
            bot.send_message(message.from_user.id, 'готово', reply_markup=start_keyboard(usero))
        else:
            bot.send_message(message.from_user.id, 'Что-то пошло не так')
            redo(message)


def prep_ismeneniya(message, args):
    cabinet, *lesson = message.text.split()
    ismeneniya(message, args[1], args[0], args[2], cabinet, ' '.join(lesson))


def ismeneniya(message, day, clas, number, cabinet, lesson):
    day = day.upper()
    db_sess = db_session.create_session()
    items = Changes()
    items.lesson_pos = number
    items.lesson = lesson
    items.cabinet = cabinet
    items.class_letter = clas
    items.day = day

    db_sess.add(items)
    db_sess.commit()
    title = db_sess.query(Changes).filter(Changes.lesson == lesson, Changes.day == day).first()
    if title:
        bot.send_message(message.from_user.id, 'Изменение было успешно сохраненно')
    else:
        bot.send_message(message.from_user.id, 'Не удалось внести изменение, попробуйте ещё раз')
    users = db_sess.query(User).filter(User.about == clas)
    for user in users:
        bot.send_message(user.user_id, f'Ваше расписание на {day} изменилось! Изменен {number} урок',
                         reply_markup=start_keyboard('завуч'))
    bot.send_message(message.from_user.id, 'Ученики были уведомлены об изменениях',
                     reply_markup=start_keyboard('завуч'))


def announce(message):
    db_sess = db_session.create_session()
    clas = message.text.split()[0]
    clas = f'{clas[:-1]} "{clas[-1].upper()}" класс'
    things_to_announce = ' '.join(message.text.split()[1:])
    students = db_sess.query(User).filter(User.user_key == clas)
    for student in students:
        bot.send_message(student.user_id, things_to_announce,
                         reply_markup=start_keyboard(message.from_user.id))
    bot.send_message(message.from_user.id, 'Сообщение отправлено',
                     reply_markup=start_keyboard(message.from_user.id))


# не нужные
'''def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url=link)
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup=markup) '''