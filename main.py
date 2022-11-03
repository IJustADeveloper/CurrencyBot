import telebot
from extensions import BaseConn, Parcer


with open("creds_file", 'r') as cf:
    creds = cf.read().split("\n")
    TOKEN = creds[3]

bot = telebot.TeleBot(TOKEN)
red = BaseConn("creds_file")


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, человек. Я бот по переводу валют.\n \n'
                                      "Если хотите узнать наименования доступных для перевода валют, "
                                      "напишите команду /values. \n\n"
                                      "Чтобы перевести деньги из одной валюты в другую отправьте сообщение вида: \n"
                                      "<код переводимой валюты> <код конечной валюты> <кол-во переводимой валюты>.\n\n"
                                      'Пример: "USD RUB 100"')


@bot.message_handler(commands=["values"])
def values(message):
    j = Parcer.parce()
    keys = j["rates"].keys()
    text = "Доступные для перевода валюты:\n"
    for i in keys:
        text += i+" - "+red.get_name(i)+"\n"
    bot.send_message(message.chat.id, text=text)


@bot.message_handler()
def calc(message):
    params = message.text.split()

    total = Parcer.get_price(params[0], params[1], params[2])
    bot.send_message(message.chat.id, text=str(total)+" "+params[1])


bot.polling(none_stop=True)
