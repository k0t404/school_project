import telebot
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, qu1, raspisanie, ismeneniya, qu2, authorization, qu3, qu4
from data import db_session
from data.keys import Keys
from data.lesssons import Lesssons
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    db_session.global_init("db/logs.db")
    db_sess = db_session.create_session()

    if message.text == '👋 Поздороваться':
        search(message)
        # ответ бота

    elif message.text == 'Расписание_уроков':
        qu1(message)

    elif message.text.split()[0] == 'Расписание':
        clas = (message.text.split())[1:]
        raspisanie(clas, message)

    elif message.text == 'Задать вопрос':
        question(message)

    elif message.text == 'Внести изменения':
        qu2(message)

    elif message.text == 'Авторизоваться':
        qu3(message)

    elif message.text.lower() == 'учитель' or message.text.lower() == 'завуч' or message.text.lower() == 'ученик':
        qu4(message)

    elif db_sess.query(Keys).filter(Keys.key_available == message.text.lower()).first():
        authorization(message)

    elif message.text.split()[0].lower() == 'авторизация':
        clas = f'{message.text.split()[1]} "{message.text.split()[2].upper()}" класс'
        print(clas, db_sess.query(Lesssons).filter(Lesssons.class_letter == clas).first())
        if db_sess.query(Lesssons).filter(Lesssons.class_letter == clas).first():
            authorization(message)
        else:
            bot.send_message(message.from_user.id, "Такого класса не существует!!!!")

    elif message.text == 'Что может бот?':
        helper(message)

    else:
        print(message.text.split())
        bot.send_message(message.from_user.id, "Используйте клавиатуру")


bot.polling(none_stop=True, interval=0)   # обязательная для работы бота часть