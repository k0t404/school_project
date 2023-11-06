import telebot
from config import BOT_TOKEN
from telebot import types
from link_to_site import link
from data import db_session
from data.items import Items
from data.users import User


bot = telebot.TeleBot(BOT_TOKEN)


def starts(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-сборщик товаров!", reply_markup=markup)


def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url=link)
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на наш сайт", reply_markup=markup)


def authorization(messag, message):
    db_sess = db_session.create_session()
    pop, email, password = messag
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Что может бот?')
        btn4 = types.KeyboardButton('Ссылка на сайт')
        btn2 = types.KeyboardButton('Добавить товар')
        btn3 = types.KeyboardButton('Удалить товар')
        btn5 = types.KeyboardButton('Вывести определённый товар')
        btn6 = types.KeyboardButton('Вывести все товары')
        markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
        bot.send_message(message.from_user.id, 'Вы прошли авторизацию, выберите действие', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn6 = types.KeyboardButton('РеАвторизация')
        markup.add(btn6)
        bot.send_message(message.from_user.id, 'Неправильная почта или пароль, попробуйте заново', reply_markup=markup)


def question(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn4 = types.KeyboardButton('Ссылка на сайт')
    btn2 = types.KeyboardButton('Добавить товар')
    btn3 = types.KeyboardButton('Удалить товар')
    btn5 = types.KeyboardButton('Вывести определённый товар')
    btn6 = types.KeyboardButton('Вывести все товары')
    markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
    bot.send_message(message.from_user.id, "Все вопросы можно писать на нашу почту")
    bot.send_message(message.from_user.id, "cot5626@mail.ru", reply_markup=markup)


def helper(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn4 = types.KeyboardButton('Ссылка на сайт')
    btn2 = types.KeyboardButton('Добавить товар')
    btn3 = types.KeyboardButton('Удалить товар')
    btn5 = types.KeyboardButton('Вывести определённый товар')
    btn6 = types.KeyboardButton('Вывести все товары')
    markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
    bot.send_message(message.from_user.id, "Я бот-справочник.")
    bot.send_message(message.from_user.id, "Я могу:")
    bot.send_message(message.from_user.id, "Вывести все выбранные вами товары")
    bot.send_message(message.from_user.id, "Вывести определенный выбранный вами товар")
    bot.send_message(message.from_user.id, "Добавить товар")
    bot.send_message(message.from_user.id, "Удaлить товар", reply_markup=markup)


def all_things(message, messag):
    db_sess = db_session.create_session()
    pop, pop2, name = messag
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn4 = types.KeyboardButton('Ссылка на сайт')
    btn2 = types.KeyboardButton('Добавить товар')
    btn3 = types.KeyboardButton('Удалить товар')
    btn5 = types.KeyboardButton('Вывести определённый товар')
    btn6 = types.KeyboardButton('Вывести все товары')
    markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
    user = db_sess.query(User).filter(User.name == name).first()
    if user:
        items = db_sess.query(Items).filter(Items.creator == name)
        if items:
            bot.send_message(message.from_user.id, f"Товары {name}:")
            for item in items:
                bot.send_message(message.from_user.id, f"{item.title}")
            bot.send_message(message.from_user.id, '', reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'У данного пользователя нет товаров', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Данный пользователь не найден', reply_markup=markup)


def one_thing(message, messag):
    pop, user_name, title = messag

    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.title == title, Items.creator == user_name).first()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn4 = types.KeyboardButton('Ссылка на сайт')
    btn2 = types.KeyboardButton('Добавить товар')
    btn3 = types.KeyboardButton('Удалить товар')
    btn5 = types.KeyboardButton('Вывести определённый товар')
    btn6 = types.KeyboardButton('Вывести все товары')
    markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
    if items:
        content = items.content
        if items.is_private:
            is_private = 'Да'
        else:
            is_private = 'Нет'
        link_to_market = items.link
        categorye = items.category
        bot.send_message(message.from_user.id, f"Данные о товаре: {title}")
        bot.send_message(message.from_user.id, f'Описание: {content}')
        bot.send_message(message.from_user.id, f"Личное:{is_private}")
        bot.send_message(message.from_user.id, f'Ссылка:{link_to_market}')
        bot.send_message(message.from_user.id, f'Категория:{categorye}', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, f'Товар не найден, попробуйте заново', reply_markup=markup)


def delete_thing(messag, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Что может бот?')
    btn4 = types.KeyboardButton('Ссылка на сайт')
    btn2 = types.KeyboardButton('Добавить товар')
    btn3 = types.KeyboardButton('Удалить товар')
    btn5 = types.KeyboardButton('Вывести определённый товар')
    btn6 = types.KeyboardButton('Вывести все товары')
    markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
    pop, user_name, title = messag
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.title == title,
                                        Items.creator == user_name
                                        ).first()
    if items:
        db_sess.delete(items)
        db_sess.commit()
        bot.send_message(message.from_user.id, "Товар успешно удалён", reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, "Товар не удалён, попробуйте заново", reply_markup=markup)


def add_thing(message, messag):
    pop, name_user, titles, content, is_private, price, link, category = messag
    db_sess = db_session.create_session()
    title = db_sess.query(Items).filter(Items.title == titles).first()
    idi = db_sess.query(User).filter(User.name == name_user).first()
    if title:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Что может бот?')
        btn4 = types.KeyboardButton('Ссылка на сайт')
        btn2 = types.KeyboardButton('Добавить товар')
        btn3 = types.KeyboardButton('Удалить товар')
        btn5 = types.KeyboardButton('Вывести определённый товар')
        btn6 = types.KeyboardButton('Вывести все товары')
        markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
        bot.send_message(message.from_user.id, 'Товар уже присутствует', reply_markup=markup)
    else:
        items = Items()
        items.title = titles
        items.content = content
        if is_private == 'да' or is_private == 'Да':
            items.is_private = True
        else:
            items.is_private = False
        items.price = price
        items.link = link
        items.creator = name_user
        items.category = category
        items.user_id = idi.id
        db_sess.add(items)
        db_sess.commit()
        title = db_sess.query(Items).filter(Items.title == titles).first()
        if title:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
            btn1 = types.KeyboardButton('Что может бот?')
            btn4 = types.KeyboardButton('Ссылка на сайт')
            btn2 = types.KeyboardButton('Добавить товар')
            btn3 = types.KeyboardButton('Удалить товар')
            btn5 = types.KeyboardButton('Вывести определённый товар')
            btn6 = types.KeyboardButton('Вывести все товары')
            markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
            bot.send_message(message.from_user.id, 'Товар добавлен успешно', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
            btn1 = types.KeyboardButton('Что может бот?')
            btn4 = types.KeyboardButton('Ссылка на сайт')
            btn2 = types.KeyboardButton('Добавить товар')
            btn3 = types.KeyboardButton('Удалить товар')
            btn5 = types.KeyboardButton('Вывести определённый товар')
            btn6 = types.KeyboardButton('Вывести все товары')
            markup.add(btn1, btn2, btn3, btn4, btn6, btn5)
            bot.send_message(message.from_user.id, 'Товар не добавлен,попробуйте заново', reply_markup=markup)