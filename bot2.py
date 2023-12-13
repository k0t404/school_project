import telebot
import os
from telebot import  types
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, raspisanie, authorization, \
    start_keyboard, announce, prep_raspisanie, prep_ismeneniya, poisk, prep_poisk, prep_raspisanie_control, unpack
from data import db_session
from data.keys import Keys
from data.lessons import Lessons
from data.users import User
from excel_to_sql import process_control
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(commands=['quit'])
def quit(message):
    db_session.global_init("db/logs.db")
    db_sess = db_session.create_session()
    user_to_quit = db_sess.query(User).filter(User.user_id == message.from_user.id)
    for user_saved in unpack(user_to_quit):
        db_sess.delete(user_saved)
    db_sess.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Авторизоваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, 'Вы успешно удалены из базы данных', reply_markup=markup)


@bot.message_handler(content_types=['document'])
def get_documents(message):
    db_session.global_init("db/logs.db")
    db_sess = db_session.create_session()
    user_check = db_sess.query(User).filter(User.user_id == message.from_user.id)
    if unpack(user_check)[0].about == 'завуч':
        if message.document.file_name.split('.')[1] == 'xlsx':
            bot.send_message(message.from_user.id, 'Файл принят')
            file_info = bot.get_file(message.document.file_id)
            excel_from_hteacher = bot.download_file(file_info.file_path)
            with open('temp_timetable.xlsx', 'wb') as file:
                file.write(excel_from_hteacher)
            db_sess.query(Lessons).delete()
            db_sess.commit()
            process_control((5, 11), file_name='temp_timetable')
            os.remove('temp_timetable.xlsx')
            bot.send_message(message.from_user.id, 'Расписание полностью изменено')
        else:
            bot.send_message(message.from_user.id, 'Неверное расширение файл (должен быть .xlsx)')
    else:
        bot.send_message(message.from_user.id, 'Не отправляйте сюда, пожалуйста, какие-либо файлы!')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    db_session.global_init("db/logs.db")
    db_sess = db_session.create_session()

    authorized_user = db_sess.query(User).filter(User.user_id == message.from_user.id).first()
    if message.text == 'Уведомление класса':
        qu = bot.send_message(message.from_user.id, 'Введите класс (слитно) и сообщение, которое хотите отправить')
        bot.register_next_step_handler(qu, announce)
    # !!!!!!!!!! вывод расписания !!!!!!!!!!!
    elif message.text == 'Расписание':
        markup_time = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Сегодняшний день")
        btn2 = types.KeyboardButton("Определенный день")
        markup_time.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Чего именно вы хотите?', reply_markup=markup_time)
    # 11111111111 вывод расписания на сегодняшний день 222222222222
    elif message.text == 'Сегодняшний день':
        if authorized_user.about.lower() == 'ученик':
            raspisanie(message, authorized_user.user_key, autharized_student=True)
        else:
            qu1 = bot.send_message(message.from_user.id, "Введите ваш класс (номер и букву)")
            bot.register_next_step_handler(qu1, prep_raspisanie)
    # @!@!@!@!@ вывод расписания на определенный день @!@!@!@!@!@
    elif message.text == 'Определенный день':
        qu1 = bot.send_message(message.from_user.id,
                               "Введите день недели (например, понедельник и т.п.) и нужный вам класс (номер и букву)")
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
        bot.send_message(message.from_user.id, "Воспользуйтесь доступными функциями бота")


bot.infinity_polling()   # обязательная для работы бота часть
