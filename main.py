import telebot
from db_connect import connection

TOKEN = "5757313852:AAGAuDwo-maawqvHfCX8V9qHaNhS51vzVRk"

red = connection(creds_file="creds_file")


bot = telebot.TeleBot(TOKEN)
bot.polling(none_stop=True)
