import telebot
from telebot import types


TOKEN = '5811022670:AAGnEXWfmIgbYxJQ0DHH8mJXTJjtqjhhddI'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    catalog = types.KeyboardButton('Каталог')
    contacts = types.KeyboardButton('Контакты')
    basket = types.KeyboardButton('Корзина')

    markup.add(catalog, contacts, basket)

    bot.send_message(message.chat.id, "Привет! Самые вкусные торты тут! 🍰", reply_markup= markup)


bot.polling(none_stop=True)
