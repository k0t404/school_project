import telebot
import datetime
from con2 import BOT_TOKEN
from telebot import types
from data import db_session
from data.lesssons import Lesssons


bot = telebot.TeleBot(BOT_TOKEN)


def starts(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я бот Артем, и я помогу тебе в расписании!", reply_markup=markup)


def search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn2 = types.KeyboardButton('Расписание_уроков')
    btn3 = types.KeyboardButton('Внести изменения')
    btn5 = types.KeyboardButton('Задать вопрос')
    markup.add(btn1, btn2, btn3, btn5)
    bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=markup)


def question(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn2 = types.KeyboardButton('Расписание_уроков')
    btn3 = types.KeyboardButton('Внести изменения')
    btn5 = types.KeyboardButton('Задать вопрос')
    markup.add(btn1, btn2, btn3, btn5)
    bot.send_message(message.from_user.id, "Все вопросы можно писать на нашу почту")
    bot.send_message(message.from_user.id, "cot5626@mail.ru", reply_markup=markup)


def helper(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn2 = types.KeyboardButton('Расписание_уроков')
    btn3 = types.KeyboardButton('Внести изменения')
    btn5 = types.KeyboardButton('Задать вопрос')
    markup.add(btn1, btn2, btn3, btn5)
    bot.send_message(message.from_user.id, "Я бот Артем.")
    bot.send_message(message.from_user.id, "Я могу:")
    bot.send_message(message.from_user.id, "Вывести расписание на сегодня")
    bot.send_message(message.from_user.id, "Внести изменения в рассписание класса")
    bot.send_message(message.from_user.id, "Играть в доту 2", reply_markup=markup)

def raspisanie(clas, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Что может бот?')
    btn2 = types.KeyboardButton('Расписание_уроков')
    btn3 = types.KeyboardButton('Внести изменения')
    btn5 = types.KeyboardButton('Задать вопрос')
    markup.add(btn1, btn2, btn3, btn5)

    days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА']
    date = days[datetime.datetime.today().weekday()]
    print(date)
    clas = f'{clas[0]}"{clas[1].capitalize()}" класс'
    print(clas)
    db_sess = db_session.create_session()
    title = db_sess.query(Lesssons).filter(Lesssons.class_letter == clas, Lesssons.day == date)
    print(title)
    if title:
        bot.send_message(message.from_user.id, f'Расписание для {clas}', reply_markup=markup)
        pass
    else:
        bot.send_message(message.from_user.id, 'Такой класс не был найден, попробуй снова', reply_markup=markup)


    # здесь нужно добавить код с подключением базы и выводом расписания

    bot.send_message(message.from_user.id, 'uu', reply_markup=markup)

def qu1(message):
    bot.send_message(message.from_user.id, "Введите: Расписание 'ваш класс(к примеру 1 ь)'")

def qu2(message):
    bot.send_message(message.from_user.id, "Введите ключ: Ключ (ваш ключ)")

def authorization(key, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Что может бот?')
    btn2 = types.KeyboardButton('Расписание_уроков')
    btn3 = types.KeyboardButton('Внести изменения')
    btn5 = types.KeyboardButton('Задать вопрос')
    markup.add(btn1, btn2, btn3, btn5)
    print(key)
    bot.send_message(message.from_user.id, 'вв', reply_markup=markup)
    # тут будет авторизация для завуча

def ismeneniya(message):
    pass

#не нужные

'''def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url=link)
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup=markup) '''