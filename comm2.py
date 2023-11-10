import telebot
import datetime
from con2 import BOT_TOKEN
from telebot import types
from data import db_session
from data.lesssons import Lesssons
from  data.users import User

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
    bot.send_message(message.from_user.id, "Внести изменения в рассписание класса")
    bot.send_message(message.from_user.id, "Играть в доту 2", reply_markup=start_keyboard())


def raspisanie(clas, message):
    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
    date = days[datetime.datetime.today().weekday()]
    clas = f'{clas[0]} "{clas[1].capitalize()}" класс'
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
    pass


def qu3(message):
    bot.send_message(message.from_user.id, "Кто вы? (Завуч/учитель/ученик")


def qu4(message):
    if message.text.lower() == 'завуч':
        bot.send_message(message.from_user.id, "Введите специальный ключ")
    if message.text.lower() == 'учитель':
        bot.send_message(message.from_user.id, "Введите специальный ключ")
    if message.text.lower() == 'ученик':
        bot.send_message(message.from_user.id, "Введите класс")


def authorization(message):
    print(1)
    print(1, message.from_user.id, message.chat.id)
    db_sess = db_session.create_session()
    user = User()
    user.user_id = message.from_user.id
    if len(message.text) == 9:
        user.about = 'завуч'
        user.hashed_password = message.text
    elif len(message.text) == 7:
        user.about = 'учитель'
        user.hashed_password = message.text
    elif len(message.text) == 4 or len(message) == 3:
        user.about = 'ученик'
        user.hashed_password = f'{message.text[0]} "{message.text[1]}" класс'
        print(f'{message.text[0]} "{message.text[1]}" класс')
    db_sess.add(user)
    db_sess.commit()
    bot.send_message(message.from_user.id, 'готово', reply_markup=start_keyboard())

def ismeneniya(message):
    pass


# не нужные
'''def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url=link)
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup=markup) '''