import telebot
from telebot import  types
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, raspisanie, authorization, \
    start_keyboard, announce, prep_raspisanie, prep_ismeneniya, poisk, prep_poisk, prep_raspisanie_control
from data import db_session
from data.keys import Keys
from data.lessons import Lessons
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
    if message.text == 'Уведомление класса':
        qu = bot.send_message(message.from_user.id, 'Введите класс (слитно) и сообщение, которое хотите отправить')
        bot.register_next_step_handler(qu, announce)
    # !!!!!!!!!! вывод расписания !!!!!!!!!!!
    # вывод расписания на сегодняшний день
    elif message.text == 'Расписание (сегодняшний день)':
        if authorized_user and authorized_user.about.lower() == 'ученик':
            print(1)
            raspisanie(message, authorized_user.user_key, autharized_student=True)
        elif not authorized_user:
            bot.send_message(message.from_user.id, "Пожалуйста, авторизуйтесь.")
            starts(message)
        else:
            qu1 = bot.send_message(message.from_user.id, "Введите ваш класс (номер и букву)")
            bot.register_next_step_handler(qu1, prep_raspisanie)
    # @!@!@!@!@ вывод расписания на определенный @!@!@!@!@!@
    # вывод расписания на сегодняшний день
    elif message.text == 'Расписание (выбранный день)':
        if not authorized_user:
            bot.send_message(message.from_user.id, "Пожалуйста, авторизуйтесь.")
            starts(message)
        else:
            qu1 = bot.send_message(message.from_user.id, "Введите день недели (например, понедельник и т.п.) и нужный вам класс (номер и букву)")
            bot.register_next_step_handler(qu1, prep_raspisanie_control)
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
                             reply_markup=start_keyboard(authorized_user.about))

    # //////// авторизация /////////
    # начало всей авторизации
    elif message.text == 'Авторизоваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Завуч")
        btn2 = types.KeyboardButton("Учитель")
        btn3 = types.KeyboardButton("Ученик")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, "Кто вы? (завуч/учитель/ученик)", reply_markup=markup)
        '''if not authorized_user:
            bot.send_message(message.from_user.id, "Кто вы? (завуч/учитель/ученик)")
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
        bot.register_next_step_handler(poisk1, prep_poisk)

    elif message.text.split()[0] == 'Поиск':
        clas = (message.text.split())[1:]
        poisk(clas, message)
    # \\\\\\\\\\ просто, чтобы было \\\\\\\\\\\
    else:
        print(message.text.split())
        bot.send_message(message.from_user.id, "Используйте клавиатуру")


bot.infinity_polling()   # обязательная для работы бота часть
