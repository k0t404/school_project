from datetime import datetime as dt
import telebot
import os
import asyncio
from telebot import types
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, raspisanie, authorization, \
    start_keyboard, announce, prep_raspisanie, prep_ismeneniya, poisk, prep_poisk, prep_raspisanie_control,\
    unpack, gen_markup, KeyboardData, raspisanie_control
from data import db_session
from data.keys import Keys
from data.lessons import Lessons
from data.users import User
from data.changes import Changes
from excel_to_sql import Timetable
from ban import Ban
bot = telebot.TeleBot(BOT_TOKEN)

db_session.global_init("db/logs.db")
kd = KeyboardData()
ban = Ban()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if str(call.from_user.id) in ban.currently_banned.keys() and time_left(call) != 0:
        if ban.bans[str(call.from_user.id)] == 0:
            bot.send_message(call.from_user.id, "Вы были заблокированы на 30 минут. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(call.from_user.id)] == 1:
            bot.send_message(call.from_user.id, "Вы были заблокированы на 1ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(call.from_user.id)] == 2:
            bot.send_message(call.from_user.id, "Вы были заблокированы на 5ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(call.from_user.id)] == 3:
            bot.send_message(call.from_user.id, "Вы были заблокированы на 24ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(call.from_user.id)] == 4:
            bot.send_message(call.from_user.id, "Вы были заблокированы на 72ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(call.from_user.id)] >= 5:
            bot.send_message(call.from_user.id, "Вы были заблокированы на 168ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        ban.checks(call.from_user.id)
        ban.ban_check(call.from_user.id)
        callback_work(call)


def callback_work(call):
    data = call.data.split('_')
    kd.classes = kd.create_classes()
    message_cb = call.message
    chat_id_cb = message_cb.chat.id
    message_id_cb = message_cb.message_id
    if data[0] == 'cbismras1':
        kd.day = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'День недели выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Пожалуйста, назовите класс",
                         reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbismras2'))
    elif data[0] == 'cbismras2':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Пожалуйста, уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbismras3'))

    elif data[0] == 'cbismras3':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Точный класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Какой по счету урок изменяете?",
                         reply_markup=gen_markup([1, 2, 3, 4, 5, 6, 7, 8], 'cbismras4'))
    elif data[0] == 'cbismras4':
        kd.lesson_pos = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Урок выбран ({data[1]})')
        qu2 = bot.send_message(call.from_user.id, "Введите кабинет и название урока (именно в таком порядке)")
        bot.register_next_step_handler(qu2, prep_ismeneniya, args=[kd.class_to_work, kd.day, kd.lesson_pos])
    elif data[0] == 'cbauth1':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbauth2'))
    elif data[0] == 'cbauth2':
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Точный класс выбран ({data[1]})')
        authorization([call.from_user.id, data[1]], student=True)
    elif data[0] == 'cbrasnow1':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbrasnow2'))
    elif data[0] == 'cbrasnow2':
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Точный класс выбран ({data[1]})')
        raspisanie(message=call, clas=data[1])
    elif data[0] == 'cbrasopr1':
        kd.day = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'День недели выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Назовите класс",
                         reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbrasopr2'))
    elif data[0] == 'cbrasopr2':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbrasopr3'))
    elif data[0] == 'cbrasopr3':
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Точный класс выбран ({data[1]})')
        kd.class_to_work = data[1]
        raspisanie_control(call, kd.class_to_work, kd.day)
    elif data[0] == 'cbsendmes1':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbsendmes2'))
    elif data[0] == 'cbsendmes2':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Точный класс выбран ({data[1]})')
        qu5 = bot.send_message(call.from_user.id,
                               "Введите сообщение, которое хотите отправить")
        bot.register_next_step_handler(qu5, announce, args=[call, kd.class_to_work])
    elif data[0] == 'cbspoisk1':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Класс выбран ({data[1]})')
        bot.send_message(call.from_user.id, "Уточните класс",
                         reply_markup=gen_markup(kd.classes[data[1]], 'cbspoisk2'))
    elif data[0] == 'cbspoisk2':
        kd.class_to_work = data[1]
        bot.edit_message_text(chat_id=chat_id_cb, message_id=message_id_cb,
                              text=f'Точный класс выбран ({data[1]})')
        poisk(kd.class_to_work, call)


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(commands=['clear_changes'])
def clear_changes(message):
    db_sess = db_session.create_session()
    user_check = db_sess.query(User).filter(User.user_id == message.from_user.id)
    if unpack(user_check)[0].about == 'завуч':
        db_sess.query(Changes).delete()
        db_sess.commit()
        bot.send_message(message.from_user.id, 'Готово')
    else:
        bot.send_message(message.from_user.id, 'У вас нет доступа на это')
    clear_changes(message)


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
                     "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    bot.send_message(message.from_user.id,
                     "Если отправить более 15 сообщений с интервалом 1.3 сек и менее, то вас заблокирует!")
    bot.send_message(message.from_user.id,
                     "Чтобы этого не случилось, достаточно подождать 3 секунды и продолжить работу со мной")
    bot.send_message(message.from_user.id,
                     "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


@bot.message_handler(commands=['quit'])
def quit(message):
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


def time_left(last_message):
    start_ban, user_id_ban, end_ban = ban.currently_banned[str(last_message.from_user.id)]
    due = dt.now() - start_ban
    need = end_ban - start_ban
    if len(str(need).split()) != 1:
        day_need, hour_need, minute_need, second_need = float((str(need).split()[0])), \
                                                        float((str(need).split()[2].split(':'))[0]), \
                                                        float((str(need).split()[2].split(':'))[0]), \
                                                        float((str(need).split()[2].split(':'))[0])
    else:
        day_need, hour_need, minute_need, second_need = 0, \
                                                        float((str(need).split(':'))[0]), \
                                                        float((str(need).split(':'))[1]), \
                                                        float((str(need).split(':'))[2])
    if len(str(due).split()) != 1:
        day_due, hour_due, minute_due, second_due = float((str(due).split()[0])),\
                                                    float((str(due).split()[2].split(':'))[0]),\
                                                    float((str(due).split()[2].split(':'))[0]),\
                                                    float((str(due).split()[2].split(':'))[0])
    else:
        day_due, hour_due, minute_due, second_due = 0, \
                                                    float((str(due).split(':'))[0]), \
                                                    float((str(due).split(':'))[1]), \
                                                    float((str(due).split(':'))[2])

    left = [abs(day_due - day_need)*24*60*60, abs(hour_due - hour_need)*60*60, abs(minute_due - minute_need)*60,
            abs(second_due - second_need)]
    seconds_left = sum(left)
    return seconds_left


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if str(message.from_user.id) in ban.currently_banned.keys() and time_left(message) != 0:
        if ban.bans[str(message.from_user.id)] == 0:
            bot.send_message(message.from_user.id, "Вы были заблокированы на 30 минут. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(message.from_user.id)] == 1:
            bot.send_message(message.from_user.id, "Вы были заблокированы на 1ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(message.from_user.id)] == 2:
            bot.send_message(message.from_user.id, "Вы были заблокированы на 5ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(message.from_user.id)] == 3:
            bot.send_message(message.from_user.id, "Вы были заблокированы на 24ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(message.from_user.id)] == 4:
            bot.send_message(message.from_user.id, "Вы были заблокированы на 72ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())
        elif ban.bans[str(message.from_user.id)] >= 5:
            bot.send_message(message.from_user.id, "Вы были заблокированы на 168ч. Причина - спам.",
                             reply_markup=types.ReplyKeyboardRemove())

    else:
        ban.checks(message.from_user.id)
        ban.ban_check(message.from_user.id)
        work(message)


def work(message):
    db_sess = db_session.create_session()
    authorized_user = db_sess.query(User).filter(User.user_id == message.from_user.id).first()
    # !!!!!!!!!! вывод расписания !!!!!!!!!!!
    if message.text == 'Расписание':
        if authorized_user:
            markup_time = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            btn2 = types.KeyboardButton("Сегодняшний день")
            btn3 = types.KeyboardButton("Определенный день")
            markup_time.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Чего именно вы хотите?', reply_markup=markup_time)
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # 11111111111 вывод расписания на сегодняшний день 222222222222
    elif message.text == 'Сегодняшний день':
        if authorized_user:
            if authorized_user.about.lower() == 'ученик':
                raspisanie(message, authorized_user.user_key)
            else:
                bot.send_message(message.from_user.id, "Выберите класс",
                                 reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbrasnow1'))
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # @!@!@!@!@ вывод расписания на определенный день @!@!@!@!@!@
    elif message.text == 'Определенный день':
        if authorized_user:
            bot.send_message(message.from_user.id, "Выберите день недели",
                             reply_markup=gen_markup(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'],
                                                     'cbrasopr1'))
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # %%%%%%%%%% задавание вопросов №№№№№№№№№
    # отправляет почту, на которую будут отправлять вопросы
    elif message.text == 'Обратная связь':
        question(message)

    # |||||||||| изменения расписания |||||||||||||
    elif message.text == 'Изменить расписание':
        if authorized_user:
            if authorized_user.about == 'завуч':
                markup_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Назад")
                btn2 = types.KeyboardButton("Определенный класс")
                btn3 = types.KeyboardButton("У всех")
                markup_table.add(btn1, btn2, btn3)
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
            bot.send_message(message.from_user.id, "Выберите класс",
                             reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbsendmes1'))
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
        bot.send_message(message.from_user.id, "Выберите класс",
                         reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbauth1'))

    # ?????????? функции бота ???????????
    # вывод функций бота, наверное
    elif message.text == 'Мои функции':
        helper(message)

    # $$$$$$$$$$ поиск класса $$$$$$$$$$
    elif message.text == 'Поиск класса':
        if authorized_user:
            bot.send_message(message.from_user.id, "Выберите класс",
                             reply_markup=gen_markup([5, 6, 7, 8, 9, 10, 11], 'cbspoisk1'))
        else:
            bot.send_message(message.from_user.id, "Вы не авторизованы. (пропишите /start)")

    # !||!|!|!|! возврат на главную !|!|!||!|!|
    elif message.text == 'Назад':
        bot.send_message(message.from_user.id, "Возвращаю.", reply_markup=start_keyboard(authorized_user.about))

    # \\\\\\\\\\ просто, что-то было \\\\\\\\\\\


bot.infinity_polling()   # обязательная для работы бота часть