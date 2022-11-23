import telebot
from telebot import types

from sql_functions import (
    SQL_register_new_user,
    SQL_get_user_data
    )


TOKEN = '5811022670:AAGnEXWfmIgbYxJQ0DHH8mJXTJjtqjhhddI'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    catalog = types.KeyboardButton('Каталог')
    contacts = types.KeyboardButton('Контакты')
    basket = types.KeyboardButton('Корзина')

    markup.add(catalog, contacts, basket)

    user_name = message.from_user.full_name
    user_login = message.from_user.username
    user_tg_id = message.from_user.id

    user = SQL_get_user_data(user_tg_id)
    if user:    # Если новый пользователь
        bot.send_message(
            message.chat.id,
            f"Welcome back {user['login']}!",
            reply_markup=markup
            )
    else:       # Если пользователь не новый
        bot.send_message(
            message.chat.id,
            f"Привет, {user_login}! Самые вкусные торты тут! 🍰",
            reply_markup=markup
            )
        SQL_register_new_user(user_name, user_login, user_tg_id)


bot.polling(none_stop=True)
