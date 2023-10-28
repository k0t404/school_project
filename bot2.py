import telebot
from con2 import BOT_TOKEN
from comm2 import starts, helper, search, question, qu1, raspisanie, ismeneniya, qu2, authorization

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    starts(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        search(message)
        # ответ бота

    elif message.text == 'Расписание_уроков':
        qu1(message)

    elif message.text.split()[0] == 'Расписание':
        clas = (message.text.split())[1]
        raspisanie(clas, message)

    elif message.text == 'Задать вопрос':
        question(message)

    elif message.text == 'Внести изменения':
        qu2(message)

    elif 'Ключ' in message.text:
        key = (message.text.split())[1]
        authorization(key, message)

    elif message.text == 'Что может бот?':
        helper(message)

    else:
        print(message.text.split())
        bot.send_message(message.from_user.id, "Используйте клавиатуру")


bot.polling(none_stop=True, interval=0)   # обязательная для работы бота часть