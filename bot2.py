import telebot
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, qu1, raspisanie, ismeneniya, qu2, authorization, qu3, qu4, \
    start_keyboard
from data import db_session
from data.keys import Keys
from data.lesssons import Lesssons
from data.users import User
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    db_session.global_init("db/logs.db")
    db_sess = db_session.create_session()

    authorized_user = db_sess.query(User).filter(User.user_id == message.from_user.id).first()
    if message.text == '👋 Поздороваться':
        search(message)
        # ответ бота

    # начало вывода расписания
    elif message.text == 'Расписание_уроков':
        if authorized_user.about == 'ученик':
            raspisanie(authorized_user.user_key, message, autharized_student=True)
        else:
            qu1(message)

    # вывод расписания на сегодняшний день
    elif message.text.split()[0] == 'Расписание':
        clas = (message.text.split())[1:]
        raspisanie(clas, message)

    # отправляет почту, на которую будут отправлять вопросы
    elif message.text == 'Задать вопрос':
        question(message)

    # здесь код Ярослава
    elif message.text == 'Внести изменения':
        if authorized_user.about == 'завуч':
            qu2(message)
        else:
            bot.send_message(message.from_user.id, "У вас нету прав для изменения в расписании",
                             reply_markup=start_keyboard())

    elif message.text.split()[0] == 'Изменение':
        if authorized_user.about == 'завуч':
            clas, number, cabinet, lesson = message.text.split()[1:]
            ismeneniya(message, clas, number, cabinet, lesson)
        else:
            bot.send_message(message.from_user.id, "У вас нету прав для изменения в расписании",
                             reply_markup=start_keyboard())

    # начало всей аторизации
    elif message.text == 'Авторизоваться':
        qu3(message)
        # Ниже финальная версия и ее нужно будет вернуть, н ос ней станет сложнее работать, т.к. мы не
        # сможем заводить новые аккунты в боте
        '''if not authorized_user:
            qu3(message)
        else:
            bot.send_message(message.from_user.id, "Вы уже авторизованы")'''

    # продолжение авторизации (определение пользователя)
    elif message.text.lower() == 'учитель' or message.text.lower() == 'завуч' or message.text.lower() == 'ученик':
        qu4(message)

    # авторизация учителей и завучей
    elif db_sess.query(Keys).filter(Keys.key_available == message.text.lower()).first():
        authorization(message)

    # авторизация учеников
    elif message.text.split()[0].lower() == 'авторизация':
        clas = f'{message.text.split()[1]} "{message.text.split()[2].upper()}" класс'
        if db_sess.query(Lesssons).filter(Lesssons.class_letter == clas).first():
            authorization(message)
        else:
            bot.send_message(message.from_user.id, "Такого класса не существует!!!!")

    # вывод функций бота, наверное
    elif message.text == 'Что может бот?':
        helper(message)
    # что это?
    # просто, чтобы было

    else:
        print(message.text.split())
        bot.send_message(message.from_user.id, "Используйте клавиатуру")


bot.polling(none_stop=True, interval=0)   # обязательная для работы бота часть