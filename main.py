import telebot
from extensions import BaseConn, Parcer, QueryException
from config import token, host, port, password


bot = telebot.TeleBot(token)
red = BaseConn(host, port, password)


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
    try:
        params = message.text.split()
        base, quote, amount = params

        if len(params) != 3:
            raise QueryException("Вы ввели слишком мало/много параметров. Попробуйте еще раз")

        total = Parcer.get_price(base, quote, amount)
    except QueryException as e:
        bot.send_message(message.chat.id, text=e)
    except Exception as e:
        bot.send_message(message.chat.id, text=f"Не удалось обработать команду.{e}")
    else:
        bot.send_message(message.chat.id, text=f"{amount} {base.upper()} = {total} {quote.upper()}")


bot.polling(none_stop=True)
