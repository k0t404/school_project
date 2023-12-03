import telebot
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, raspisanie, authorization, \
    start_keyboard, announce, prep_raspisanie, prep_ismeneniya, poisk, prep_poisk
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
    # !!!!!!!!!! вывод расписания !!!!!!!!!!!
    # вывод расписания на сегодняшний день
    elif message.text == 'Расписание_уроков':
        if authorized_user and authorized_user.about == 'ученик':
            raspisanie(message, authorized_user.user_key, autharized_student=True)
        else:
            qu1 = bot.send_message(message.from_user.id, "Введите ваш класс (номер и букву)")
            bot.register_next_step_handler(qu1, prep_raspisanie)
    # %%%%%%%%%% задавание вопросов №№№№№№№№№
    # отправляет почту, на которую будут отправлять вопросы
    elif message.text == 'Задать вопрос':
        question(message)

    # |||||||||| изменения расписания |||||||||||||
    elif message.text == 'Внести изменения':
        if authorized_user and authorized_user.about == 'завуч':
            qu2 = bot.send_message(message.from_user.id,
                                   "Введите номер и букву класса (слитно), номер урока, кабинет, название урока")
            bot.register_next_step_handler(qu2, prep_ismeneniya)
        else:
            bot.send_message(message.from_user.id, "У вас нет прав для изменения расписания",
                             reply_markup=start_keyboard(message.from_user.id))

    # //////// авторизация /////////
    # начало всей аторизации
    elif message.text == 'Авторизоваться':
        bot.send_message(message.from_user.id, "Кто вы? (Завуч/учитель/ученик)")
        # Ниже финальная версия и ее нужно будет вернуть, н ос ней станет сложнее работать, т.к. мы не
        # сможем заводить новые аккунты в боте
        '''if not authorized_user:
            bot.send_message(message.from_user.id, "Кто вы? (Завуч/учитель/ученик)")
        else:
            bot.send_message(message.from_user.id, "Вы уже авторизованы")'''

    elif message.text.lower() == 'завуч':
        qu3_1 = bot.send_message(message.from_user.id, "Введите специальный ключ")
        bot.register_next_step_handler(qu3_1, authorization)

    elif message.text.lower() == 'учитель':
        qu3_2 = bot.send_message(message.from_user.id, "Введите специальный ключ")
        bot.register_next_step_handler(qu3_2, authorization)

    elif message.text.lower() == 'ученик':
        qu3_3 = bot.send_message(message.from_user.id, "Введите номер и букву класса (именно в этом порядке)")
        bot.register_next_step_handler(qu3_3, authorization)
    # ........ отправка сообщения классу .........
    elif message.text == 'Отправить сообщение классу':
        if authorized_user and authorized_user.about != 'ученик':
            qu5 = bot.send_message(message.from_user.id,
                                   "Введите номер и букву класса (через пробел) и сообщение, которое хотите передать")
            bot.register_next_step_handler(qu5, announce)

        elif authorized_user and authorized_user.about == 'ученик':
            bot.send_message(message.from_user.id, "У вас нет доступа к данной функции")

        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы.")
    # ?????????? функции бота ???????????
    # вывод функций бота, наверное
    elif message.text == 'Что может бот?':
        helper(message)
    # $$$$$$$$$$ поиск класса $$$$$$$$$$
    elif message.text == 'Поиск класса':
        poisk1 = bot.send_message(message.from_user.id, "Введите класс, который вам нужен")
        bot.register_next_step_handler(poisk1, prep_poisk())

    elif message.text.split()[0] == 'Поиск':
        clas = (message.text.split())[1:]
        poisk(clas, message)
    # \\\\\\\\\\ просто, чтобы было \\\\\\\\\\\
    else:
        print(message.text.split())
        bot.send_message(message.from_user.id, "Используйте клавиатуру")


bot.polling(none_stop=True, interval=0)   # обязательная для работы бота часть
