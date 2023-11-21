import telebot
import datetime
from con2 import BOT_TOKEN
from telebot import types
from data import db_session
from data.lesssons import Lesssons
from  data.users import User
from data.changes import Changes

bot = telebot.TeleBot(BOT_TOKEN)


def start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn2 = types.KeyboardButton('Расписание_уроков')
    btn3 = types.KeyboardButton('Внести изменения')
    btn4 = types.KeyboardButton('Авторизоваться')
    btn5 = types.KeyboardButton('Задать вопрос')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def starts(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я бот Артем, и я помогу тебе в расписании!",
                     reply_markup=start_keyboard())


def search(message):
    bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=start_keyboard())


def question(message):
    bot.send_message(message.from_user.id, "Все вопросы можно писать на нашу почту")
    bot.send_message(message.from_user.id, "cot5626@mail.ru", reply_markup=start_keyboard())


def helper(message):
    bot.send_message(message.from_user.id, "Я бот Артем.")
    bot.send_message(message.from_user.id, "Я могу:")
    bot.send_message(message.from_user.id, "Вывести расписание на сегодня")
    bot.send_message(message.from_user.id, "Внести изменения в рассписание класса", reply_markup=start_keyboard())


def raspisanie(clas, message, autharized_student=False):
    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
    if autharized_student:
        clas = clas
    else:
        clas = f'{clas[0]} "{clas[1].capitalize()}" класс'

    if datetime.datetime.today().weekday() > 4:
        bot.send_message(message.from_user.id, 'Бот отказывается работать в выходные. Иди к МЭШ-у',
                         reply_markup=start_keyboard())
    else:
        date = days[datetime.datetime.today().weekday()]
        db_sess = db_session.create_session()
        lessons = []
        for row in db_sess.query(Lesssons).filter(Lesssons.class_letter == clas, Lesssons.day == date):
            lesson = [row.lesson_pos, row.lesson, row.cabinet, row.class_letter, row.day]
            lessons.append(lesson)
        if lessons:
            bot.send_message(message.from_user.id, f'Расписание для {clas}', reply_markup=start_keyboard())
            for row in lessons:
                if None not in row:
                    bot.send_message(message.from_user.id, '       '.join(row), reply_markup=start_keyboard())
        else:
            bot.send_message(message.from_user.id, 'Такой класс не был найден, попробуй снова',
                             reply_markup=start_keyboard())


def qu1(message):
    bot.send_message(message.from_user.id, "Введите: Расписание 'ваш класс(к примеру 1 ь)'")

def qu2(message):
    bot.send_message(message.from_user.id, "Введите: Изменение 'класс номер_урока кабинет название_урока")


def qu3(message):
    bot.send_message(message.from_user.id, "Кто вы? (Завуч/учитель/ученик)")


def qu4(message):
    if message.text.lower() == 'завуч':
        bot.send_message(message.from_user.id, "Введите специальный ключ")
    if message.text.lower() == 'учитель':
        bot.send_message(message.from_user.id, "Введите специальный ключ")
    if message.text.lower() == 'ученик':
        bot.send_message(message.from_user.id,
                         "Введите следующие слова (без ковычек). 'авторизация номер_класса буква_класса'")


def authorization(message):
    db_sess = db_session.create_session()
    user = User()
    user.user_id = message.from_user.id
    if len(message.text) == 9:
        user.about = 'завуч'
        user.user_key = message.text
    elif len(message.text) == 7:
        user.about = 'учитель'
        user.user_key = message.text
    elif len(message.text.split()) == 3:
        user.about = 'ученик'
        user.user_key = f'{message.text.split()[1]} "{message.text.split()[2].upper()}" класс'
        print(f'{message.text[0]} "{message.text[1]}" класс')
    db_sess.add(user)
    db_sess.commit()
    bot.send_message(message.from_user.id, 'готово', reply_markup=start_keyboard())


def ismeneniya(message, clas, number, cabinet, lesson):
    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
    if datetime.datetime.today().weekday() > 4:
        bot.send_message(message.from_user.id, 'В выходные невозможно вносить изменения',
                         reply_markup=start_keyboard())
    else:
        date = days[datetime.datetime.today().weekday()]
        db_sess = db_session.create_session()
        items = Changes()
        items.lesson_pos = number
        items.lesson = lesson
        items.cabinet = cabinet
        items.class_letter = clas
        items.day = date
        db_sess.add(items)
        db_sess.commit()
        title = db_sess.query(Changes).filter(Changes.lesson == lesson, Changes.day == date).first()
        if title:
            bot.send_message(message.from_user.id, 'Изменение было успешно сохраненно', reply_markup=start_keyboard())
        else:
            bot.send_message(message.from_user.id, 'Не удалось внести изменение, попробуйте ещё раз', reply_markup=start_keyboard())



def search_for(message):
    pass


# не нужные
'''def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url=link)
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup=markup) '''