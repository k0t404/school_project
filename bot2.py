import telebot
import os
from telebot import types
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, raspisanie, authorization, \
    start_keyboard, announce, prep_raspisanie, prep_ismeneniya, poisk, prep_poisk, prep_raspisanie_control,\
    unpack, gen_markup, KeyboardData
from data import db_session
from data.keys import Keys
from data.lessons import Lessons
from data.users import User
from excel_to_sql import Timetable
bot = telebot.TeleBot(BOT_TOKEN)


kd = KeyboardData()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    kd.classes = kd.create_classes()
    if data[0] == 'cbismras1':
        kd.day = data[1]
        bot.send_message(call.from_user.id, "Пожалуйста, назовите класс",
                         reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbismras2'))
    elif data[0] == 'cbismras2':
        kd.class_to_work = data[1]
        bot.send_message(call.from_user.id, "Пожалуйста, уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbismras3'))
    elif data[0] == 'cbismras3':
        kd.class_to_work = data[1]
        bot.send_message(call.from_user.id, "Какой по счету урок изменяете?",
                         reply_markup=gen_markup([1, 2, 3, 4, 5, 6, 7, 8], 'cbismras4'))
    elif data[0] == 'cbismras4':
        kd.lesson_pos = data[1]
        qu2 = bot.send_message(call.from_user.id, "Введите кабинет и название урока (именно в таком порядке)")
        bot.register_next_step_handler(qu2, prep_ismeneniya, args=[kd.class_to_work, kd.day, kd.lesson_pos])
    elif data[0] == 'cbras1':
        kd.class_to_work = data[1]
        bot.send_message(call.from_user.id, "Уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbras2'))
    elif data[0] == 'cbras2':
        authorization([call.from_user.id, data[1]], student=True)


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Я бот Артем.")
    bot.send_message(message.from_user.id, "Я могу:")
    bot.send_message(message.from_user.id, "Вывести расписание на сегодня")
    bot.send_message(message.from_user.id, "Внести изменения в расписание класса")
    bot.send_message(message.from_user.id, "Отправить сообщение классу")
    bot.send_message(message.from_user.id, "Напишите /quit, чтобы выйти из базы данных пользователей")
    bot.send_message(message.from_user.id, "Напишите /start, чтобы начать авторизацию по новой")
    bot.send_message(message.from_user.id, "Напишите /help, чтобы увидеть это же сообщение")
    bot.send_message(message.from_user.id,
                     "При неправильном вводе повторяйте весь процесс заново, не надо отправлять сообщения несколько раз")


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
            Timetable().process_control((5, 11), file_name='temp_timetable')
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
    '''print(unpack(authorized_user))'''
    # !!!!!!!!!! вывод расписания !!!!!!!!!!!
    if message.text == 'Расписание':
        if authorized_user:
            markup_time = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Сегодняшний день")
            btn2 = types.KeyboardButton("Определенный день")
            markup_time.add(btn1, btn2)
            bot.send_message(message.from_user.id, 'Чего именно вы хотите?', reply_markup=markup_time)
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # 11111111111 вывод расписания на сегодняшний день 222222222222
    elif message.text == 'Сегодняшний день':
        if authorized_user:
            if authorized_user.about.lower() == 'ученик':
                raspisanie(message, authorized_user.user_key, autharized_student=True)
            else:
                qu1 = bot.send_message(message.from_user.id, "Введите ваш класс (номер и букву)")
                bot.register_next_step_handler(qu1, prep_raspisanie)
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # @!@!@!@!@ вывод расписания на определенный день @!@!@!@!@!@
    elif message.text == 'Определенный день':
        if authorized_user:
            qu1 = bot.send_message(message.from_user.id,
                                   "Введите день недели (например, понедельник и т.п.) и нужный вам класс (номер и букву)")
            bot.register_next_step_handler(qu1, prep_raspisanie_control)
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # %%%%%%%%%% задавание вопросов №№№№№№№№№
    # отправляет почту, на которую будут отправлять вопросы
    elif message.text == 'Задать вопрос':
        question(message)

    # |||||||||| изменения расписания |||||||||||||
    elif message.text == 'Изменить расписание':
        if authorized_user:
            if authorized_user.about == 'завуч':
                markup_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Определенный класс")
                btn2 = types.KeyboardButton("У всех")
                markup_table.add(btn1, btn2)
                bot.send_message(message.from_user.id, 'Выберите вид изменения', reply_markup=markup_table)
            else:
                bot.send_message(message.from_user.id, "У вас нет прав для изменения расписания",
                                 reply_markup=start_keyboard(authorized_user.about))
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")
    elif message.text == 'Определенный класс':
        if authorized_user:
            if authorized_user.about == 'завуч':
                bot.send_message(message.from_user.id, "Пожалуйста, выберите день недели",
                                 reply_markup=gen_markup(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'],
                                                         'cbismras1'))
            else:
                bot.send_message(message.from_user.id, "У вас нет прав для изменения расписания",
                                 reply_markup=start_keyboard(authorized_user.about))
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")
    elif message.text == 'У всех':
        if authorized_user:
            if authorized_user.about == 'завуч':
                bot.send_message(message.from_user.id, 'Отправьте .xlsx таблицу с новым расписанием 5-11 классов',
                                 reply_markup=start_keyboard(authorized_user.about))
            else:
                bot.send_message(message.from_user.id, "У вас нет прав для изменения расписания",
                                 reply_markup=start_keyboard(authorized_user.about))
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # ........ отправка сообщения классу .........
    elif message.text == 'Отправить сообщение классу':
        if authorized_user and authorized_user.about != 'ученик':
            qu5 = bot.send_message(message.from_user.id,
                                   "Введите номер и букву класса (через пробел) и сообщение, которое хотите передать")
            bot.register_next_step_handler(qu5, announce)
        elif authorized_user and authorized_user.about == 'ученик':
            bot.send_message(message.from_user.id, "У вас нет доступа к данной функции")
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # //////// авторизация /////////
    # начало всей авторизации
    elif message.text == 'Авторизоваться':
        KeyboardData.user_id = message.from_user.id
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
        bot.send_message(message.from_user.id, "Пожалуйста, выберите день недели",
                         reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbras1'))

    # ?????????? функции бота ???????????
    # вывод функций бота, наверное
    elif message.text == 'Памятка':
        helper(message)

    # $$$$$$$$$$ поиск класса $$$$$$$$$$
    elif message.text == 'Поиск класса':
        if authorized_user:
            poisk1 = bot.send_message(message.from_user.id, "Введите класс, который вам нужен")
            bot.register_next_step_handler(poisk1, prep_poisk)
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")
    elif message.text.split()[0] == 'Поиск':
        if authorized_user:
            clas = (message.text.split())[1:]
            poisk(clas, message)
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # \\\\\\\\\\ просто, чтобы было \\\\\\\\\\\
    else:
        print(message.text.split())
        bot.send_message(message.from_user.id, "Воспользуйтесь доступными функциями бота")


bot.infinity_polling()   # обязательная для работы бота часть
